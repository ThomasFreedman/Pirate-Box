#!/usr/bin/env python3
#
# ytdlVideoGrabber.py - Program to scrape videos and add them to IPFS.
#
# A SQLite3 database is used to  store  IPFS  hashes and detailed metadata for
# each  video.  This  lightweight  SQL engine is filesystem based (no server).
#
# This script requires 2 JSON formatted config files containing  schema column
# names and other info, like filter settings for video length and upload date.
#
# Youtube is known to change the metadata keys, making it difficult to rely on
# youtube metadata for the schema. After sampling 1000s of videos a common set
# of metadata fields was arrived at. The metadataFields.json file is currently
# where these fields / database columns are defined.
#
# The metadata provided by youtube-dl extractors is not totally normalized. To
# insure a database record is saved for every file added to IPFS, an alternate
# metadata dictionary is used which always sets these 9 essential columns:
#
# sqlts, pky, g_idx, grupe, vhash, vsize, season_number, url and _filename
#
# and any others from the downloaded metadata whose  field  names  are found in
# the metadataField.json file.  A substitute metadata dictionary is used when a
# SQL error occurs while adding a new row. If the 2nd attempt fails it's logged
# along with the IPFS hash,  so a record can be added manually at a later time.
# Usually the substitution is  required because there are missing fields in the
# metadata provided by some youtube-dl extractors specific to a video source.
#
from __future__ import unicode_literals
from email.message import EmailMessage
from ytdlServerDefinitions import *        # Server specific CONSTANTS
from youtube_dl import utils
from tinytag import TinyTag                # To get meta info from MP3 files
from datetime import *
import youtube_dl
import subprocess
import threading
import smtplib
import sqlite3
import time
import json
import ssl
import sys
import os
import re


#
# Global Variables
#
SQLrows2Add     = []    # Lists populated by download callback threads
ErrorList       = []

# Loaded from config file specified on command line (JSON file format).
# This variable will remain empty until the config file is read.
Config = {}

"""  Config file template, JSON format. Use single quotes only, null not None:
Config {
     "Comment": [ "Unreferenced - for comments inside config file",
        "It is difficult sometimes to find the video link for Brightcove videos.",
        "This is the method that I use with Firefox. You will need 2 things:",
        "a) AccountID",
        "b) VideoID",
        "Get these by right-clicking on the video and select Player Information.",
        "Use ctrl-C to copy the info, and plug them into this template:",
        "http://players.brightcove.net/<AccountID>/default_default/index.html?videoId=<VideoID>",
        "Works with Firefox 68.8, 75.0 and probably others as of May 12, 2020"
    ],

    "DLbase":    "dir",      Folder for all downloaded files organized by grupe
    "DLeLog":    "file",     File for exceptions / errors during downloads
    "DLarch":    "file",     This tracks downloads to skip those already done
    "DLmeta":    "file",     The metadata definition is now split into this file

    "DLOpts": {              Name / value pairs for youtube-dl options
        "optName1": "value1", NOT always the same as cmd line opts
        ...
    },

    "Grupes": {    # Dictionary of grupes to download, with its own criteria
        "gName1": {          Group name containing video selection criteria
            "Active": true,  Enable or disable downloads for this grupe
            "Duration":  0,  Min size of video in seconds; for no limits use 0
            "Quota":  null,  Limits size of grupe's DL folder to N files
            "Start":  null,  Earliest upload date string or (YYYYMMDD) or null
            "End":    null,  Latest upload date or null. 1, 2 or neither OK
            "Stop":   null,  Stop downloading from playlist after this many DLs
                "url1",
                "url2",
                ...
            ]
        },
        ...                  Additional grupes
    },

    "MetaColumns": [   Contains the list of database fields for metadata for
        ...            the video downloaded along with it in JSON format.
                       This section is loaded from a separate file defined
                       next.
    ]
}
"""


def usage():
    cmd =  sys.argv[0]
    str =  "\nUses youtube-dl to download videos and add them to IPFS and track\n"
    str += "the results in a SQLite database.\n\n"
    str += "Usage:  " + cmd + " [-h] | <-c config> <-d sqlite> [-g grupe]\n"
    str += "-h or no args print this help message.\n\n"
    str += "-c is a JSON formated config file that specifies the target groups,\n"
    str += "their URL(s),  the list of metadata columns, downloader options and\n"
    str += "the base or top level folder for the groups of files downloaded.\n"
    str += "-d is the SQLite filename (it is created if it doesn't exist).\n\n"
    str += "-g ignore all but the grupes in config except the one name after -g.\n\n"
    print(str)
    exit(0)


# Flattens a nested JSON object and returns a python dictionary
def flatten_json(nested_json):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


# Create the SQLite database file if it doesn't  exist,  using the
# MetaColumns from Config. If it already exists, open a connection
# to it. Always returns a connection object to the dbFile.
def openSQLiteDB(columns, dbFile):
    newDatabase = not os.path.exists(dbFile)
    conn = sqlite3.connect(dbFile)
    if newDatabase:
        sql = '''create table if not exists IPFS_INFO (
        "sqlts"     TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
        "pky"       INTEGER PRIMARY KEY AUTOINCREMENT,
        "db_hash"   TEXT,
        "dl_good"   INTEGER DEFAULT 0,
        "dl_errs"   INTEGER DEFAULT 0);'''
        conn.execute(sql)

        sql = '''create table if not exists IPFS_HASH_INDEX (
        "sqlts" TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
        "pky"   INTEGER PRIMARY KEY AUTOINCREMENT,
        "g_idx" TEXT,
        "grupe" TEXT,
        "vhash" TEXT,
        "vsize" TEXT,
        "mhash" TEXT'''
        for c in columns:
            sql += ',\n\t"' + c + '" TEXT'
        sql += ')'
        conn.execute(sql)
    return conn


# Add a file to IPFS and return the hash for it. Needs some error detection
def add2IPFS(file):
    lst = []
    cmd = ["ipfs", "add", file]
    out = subprocess.run(cmd, stderr=subprocess.DEVNULL,
                              stdout=subprocess.PIPE).stdout.decode('utf-8')
    return out.split("\n")[0][6:52]     # Only take the 46 character hash


# Add the updated SQLite DB to IPFS under the static IPNS name associated with
# STATIC_DB_HASH. That way the most recent DB can always be obtained by wget:
# https://ipfs.io/ipns/<STATIC_DB_HASH value>. 
def publishDB(file):
    newDBhash = add2IPFS(file)  # Add the updated SQLite database to IPFS
    if len(newDBhash) == 46:
        if STATIC_DB_HASH:
            lst = []
            cmd = ["ipfs", "name", "publish", "-key=" + STATIC_DB_HASH, newDBhash]
            cp = subprocess.run(cmd, capture_output=True, text=True)
            if cp.returncode == 0:
                published = cp.stdout[77:123]  # Grab the last hash in output
            else:
                print(cp.stderr)
    return newDBhash


# Reopen the SQL DB and update the IPFS_INFO table with info for this run.
def updateRunInfo(config, sqlFile, dbHash, good, errs):
    conn = openSQLiteDB(config['MetaColumns'], sqlFile)
    conn.row_factory = sqlite3.Row  # Results as python dictionary
    sql = '''INSERT INTO IPFS_INFO ("db_hash", "dl_good", "dl_errs")
             VALUES (?,?,?);'''

    if conn is not None:
        conn.execute(sql, (dbHash, good, errs))
        conn.commit()
        conn.close()


# Filter the list of URLs provided in config file to skip URLs we've already
# DL'd. Filtering is based on the video ID for single videos only. This isn't
# of much value b/c most URLs are for a channel or playlist.
def filterUrls(conn, configUrls):
    regx = re.compile(r'^.*?watch\?v=([^&]+)&*.*$', re.IGNORECASE)
    cursor = conn.cursor()
    filteredUrls = []
    for url in configUrls:
        match = re.search(regx, url)
        if match is not None:   # Is this a single video url?
            id = match.group(1)
            sql = "SELECT COUNT(*) FROM IPFS_HASH_INDEX WHERE id = ?;"
            if cursor.execute(sql, [id]).fetchone()[0] == 0:
                filteredUrls.append(url)
        else: filteredUrls.append(url)
    return filteredUrls



# Create a grupe index file containing a list of all video and metadata IPFS
# hashes for the grupe. Add it to IPFS & return the hash and count of rows
# updated.
def updateGrupeIndex(conn: object, grupe: object) -> object:
    cursor = conn.cursor()

    idxFile = "/tmp/%s_idx.txt" % grupe
    idx = open(idxFile, "w")
    sql =  'SELECT "v=" || vhash || " " || "m=" || mhash'
    sql += '  FROM IPFS_HASH_INDEX'
    sql += ' WHERE grupe = "%s"' % grupe
    for row in cursor.execute(sql): # Loop through all rows this grupe
        idx.write(row[0] + "\n")
    idx.close()
    hash = add2IPFS(idxFile)
    if len(hash) > 0:
        sql = "UPDATE IPFS_HASH_INDEX set g_idx=? WHERE grupe=?"
        cursor.execute(sql, (hash, grupe))
        conn.commit()
        os.remove(idxFile)
    return cursor.rowcount, hash


#    This block of code will create group index files for every group in DB,
#    then add that file to IPFS. Update every row in the group with that hash,
#    and do that for every grupe, so every row in IPFS_HASH_INDEX table gets
#    updated. See "updateGrupeIndex" above for details. This just wraps that.
def regenerateAllGrupeIndexes(conn):
    cursor = conn.cursor()
    sql = "sSELECT DISTINCT grupe FROM IPFS_HASH_INDEX"
    for row in cursor.execute(sql):
        (count, hash) = updateGrupeIndex(conn, row[0])
        print("Updated %d rows for grupe %s with grupe index hash %s" %
               (count, row[0], hash))


# Add a row to SQLite database. Most of the column data is from the JSON
# metadata (gvmjList) downloaded with the video. Note that SQLite is not
# thread safe, so only the main thread updates the DB.
def addRow2db(conn, cols, gvmjList):
    (grupe, vhash, vsize, mhash, jsn) = gvmjList
    cursor = conn.cursor()
    jsn["episode_number"] = mhash # Mark row as pinned by adding the hashes
    jsn["season_number"] = vhash  #  to these fields
    values = [grupe, vhash, vsize, mhash]  # 1st 4 values not in YT metadata
    sql    = 'INSERT INTO IPFS_HASH_INDEX ("grupe", "vhash", "vsize", "mhash"'

    for col in cols:
        sql += ',\n\t"' + col + '"'

    sql += ") VALUES (?,?,?,?"       # Now add metadata
    for col in cols:
        sql += ",?"
        values.append(jsn[col])
    sql += "); "

    cursor.execute(sql, values)
    conn.commit()

    return cursor.lastrowid


# This wrapper function detects failures in the addRow2db  function above and
# makes a 2nd attempt to insert the row with alternate metadata dictonary. If
# the failure occurs on the second attempt the failure is indicated by a None
# return value and raising the SQLite3 exception. A new dictionary is created
# and all valid metadata values in download are copied to it.  Missing values
# are set to "?".
#
# The ytdl  extractors vary as to the the format of the metadata they produce,
# youtube-dl doesn't totally normalize it.  If a video file was downloaded and
# an IPFS hash was produced a row will be added with sqlts, pky, g_idx, grupe,
# vhash, vsize, season_number and _filename columns that have known valid data.
def addRow(conn, cols, gvmjList):
    try:
        row = addRow2db(conn, cols, gvmjList)   # Attempt number one...

    # On failure create a new metadata dictionary for this file. For any
    # missing keys, create a key whose value is "?". This is a work-
    # around for JSON metadata fields the extractor doesn't provide.
    except (sqlite3.OperationalError, KeyError) as e:
        newDictionary = {}
        (grp, vhash, vsize, mhash, jsn) = gvmjList
        for col in cols:
            # If this download is an MP3 file and source is not youtube,
            #   pull some info directly from ID3 tags of the MP3 file.
            if col == "_filename":
                file = jsn[col]
                type = file.rsplit('.')[1].lower()
                ytdl = jsn["extractor"]
                if type == "mp3" and ytdl != "youtube":
                    id3 = TinyTag.get(file)
                    if id3.year : jsn["release_year"] = id3.year
                    if id3.title: jsn["title"] = id3.title
                    if id3.artist: jsn["artist"] = id3.artist
                    if id3.duration: jsn["duration"] = id3.duration

            if col in jsn.keys():
                newDictionary[col] = jsn[col]
            else: newDictionary[col] = "?"         # Previously "unknown-value"

        # Try again. Any exception this time will propagate upstream
        if col == "abr":
            print(f"lcols={len(cols)} {cols}\n\nldic={len(newDictionary)} {newDictionary.keys()}")
            exit(0)

        row = addRow2db(conn, cols, (grp, vhash, vsize, mhash, newDictionary))

    return row


# Add a row to the SQLite database for every video  downloaded for this grupe,
# print the successes and failures and log the failures to the error log file.
# NOTE: Reduced printed output for Pirate Box for leaner reporting.
def processGrupeResults(conn, cols, urls, grupe, eLog):
    global ErrorList, SQLrows2Add
    downloads = len(SQLrows2Add)
    good = 0

    if downloads > 0:
        for dat in SQLrows2Add:  # dat = (grp, vhash, vSize, mhash, json)
            try:
                row = addRow(conn, cols, dat)
                good += 1   # Sucessfully added to SQLite
#                mark = datetime.now().strftime("%a %H:%M:%S")
#                refs = "video=%s, metadata=%s" % (dat[1], dat[3])
#                print("%s row=%d, %s" % (mark, row, refs))

            # Failed to add the row to SQLite, but it's saved in IPFS
            except Exception as expn:
                args = (dat[0], dat[1], dat[2], dat[3], dat[4], expn)
                er = "SQL Error! Grupe=%s vHash=%s mHash=%s JSON=%s\n%s" % args
#                print(er)
                er += "\nMetadata key/values used:\n"
                for col in dat[4]:
                    er += "%32s = %s\n" % (col, dat4[col])
                ErrorList.append(er)

#        print("%d downloads, %d DB rows added" % (downloads, good))
        args = (updateGrupeIndex(conn, grupe))
#        print("Updated %d rows with grupe index hash %s\n" % args)

    # Print and log the list of download failures
    failures = len(ErrorList)
    if len(ErrorList) > 0:
        eLog.write("PROCESSING ERRORS FOR GRUPE=%s:\n" % grupe)
        for error in ErrorList:
            eLog.write(error + '\n')
        eLog.write("END OF ERRORS FOR %s\n\n" % grupe)

    args = (urls, downloads, failures)
    print("URLs Processed=%d (Succeeded=%d, Failed=%d)" % args)
    return good, failures


# Used to determine if folder size limit has been exceeded. NOT recursive
def getSize(path):
    totalSize = 0
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        totalSize += os.path.getsize(fp)
    return totalSize


# Check if the download folder for this grupe is over the quota (if any)  and
# remove the oldest file if it is.  The quota  is the maximum number of files
# or the maximum amount of space to limit the folder to. Quota is a string of
# integers followed by whitespace & unit string value. If no unit designation
# is specified the quota is the amount of space used in bytes. When the limit
# is exceeded the oldest files are removed to make room. .json and .wav files
# aren't counted in a file count quota, but they are for folder space quotas.
# Removals always remove all files of the same name  regardless of extension,
# HOWEVER, wildcard replacement occurs after the 1st . on the left. Also note
# that pruning will never remove the last remaining file.
def pruneDir(quota, dir):
    global ErrorList
    max = count = 0
    fList = []

    if quota:                               # Do nothing if no quota specified
        q = quota.split(' ')                # Quota amount and units, if any
        if q[0].isdecimal():                # Check if string is a valid number
            max = int(q[0])                 # This is the quota limit
        if max < 2:                         # Invalid quota value, zero removed
            err = "Invalid quota: " + dir
            ErrorList.append(err)           # Log the error
            return False

        for f in os.listdir(dir):           # Create a list of candidate files
            if f.endswith(EXT_LIST):        # Only include primary video files
                fList.append(dir + '/' + f) # Prefix the file with path
                count += 1                  # Count how many in the list
        if count < 2: return False          # We're done if none or only 1

        old = min(fList, key=os.path.getctime)   # Get oldest file

        if len(q) > 1: size = 0             # Quota limits number of files
        else: size = getSize(dir)           # Quota limits space used
        if count > max or size > max:       # Over the quota?
            rm = old.rsplit('.')[0] + ".*"  # Replace extension with a wildcard
            os.system("rm -rf %s" % rm)     # Easy way to do all related files
            return True                     # Oldest file removed
        else: return False


# This function is a process thread started with each successful download. It
# is started as a daemon thread to add the video and its' metadata to IPFS,
# and creates lists for errors and the files downloaded (to update SQLite).
def processVideo(file):
    global Config, ErrorList, SQLrows2Add
    vHash = mHash = jFlat = None

    grp = file.rsplit('/', 2)[1]      # Extract grupe from file pathname
    pb = os.path.splitext(file)[0]    # Path + Basename in list index 0
    mFile = pb + ".info.json"         # json metadata file for this download
    vFile = file                      # Full pathname of downloaded file
    dir, base = file.rsplit('/', 1)   # Separate grupe folder & downloaded file
    vSize = os.path.getsize(vFile)    # Get the size of this file for database
    print(f"vsize={vSize}")

    # The grupe quota limits the size of the download folder. It's a string
    # containing an integer with a space followed by an optional units word.
    quota = Config["Grupes"][grp]["Quota"] # i.e. "20 files" or "2500000000"
    pruned = False
    while pruneDir(quota, dir):        # Keep pruning until under quota
        time.sleep(0.01)
        pruned = True
    if pruned: ErrorList.append("WARNING: Folder limit reached and pruned!")

    # Log all errors, but add to SQLite if we got a valid video hash from IPFS
    try:
        vHash = add2IPFS(vFile)           # Add video file to IPFS
        mHash = add2IPFS(mFile)           # Add the metadata file to IPFS
        if len(vHash) + len(mHash) == 92: # Continue if valid hashes
            with open(mFile, 'r') as jsn: # Read the entire JSON metadata file
                jDict = json.load(jsn)    # Create a python dictionary from it
            jFlat = flatten_json(jDict)   # Flatten the dictionary

    except Exception as e:             # Log any errors that may have occurred
        args = (grp, vHash, mHash, base, e)
        ErrorList.append("Grupe=%s vHash=%s mHash=%s vFile=%s\n%s" % args)

    # If vHash is valid create a SQLite entry for it, regardless of metadata
    finally:
        if len(vHash) == 46 and vHash[0] == 'Q':
            SQLrows2Add.append([grp, vHash, vSize, mHash, jFlat])   # add to DB
#            os.remove(file)               # Delete after adding to IPFS
# This "appears" to mess up adding to entries to the database


# Starts a daemon thread to process the downloaded file. youtube-dl provides no
# way to obtain information about the ffmpeg post processor, and adding to IPFS
# can be time consuming.  Using  threads to handle files allows the main thread
# 2 download other files concurrently with IPFS additions. See the processVideo
# function above for specifics of how downloaded files are processed.
def callback(d):
    if d['status'] == 'finished':
        path = d['filename']             # Callback provides full pathname
        th = threading.Thread(target=processVideo, args=([path]), daemon=True)
        th.start()                       # Start the thread and continue


##############################################################################
#                                                                            #
# Primary program loop. The  youtube-dl library  takes care of downloading.  #
# The callback function above processes each download, adding files to IPFS  #
# and creating a list of rows to add to the SQLite DB by this function.      #
#                                                                            #
##############################################################################
def ytdlProcess(config, conn):
    global          ErrorList, SQLrows2Add
    sep             = SEPARATOR
    cols            = config['MetaColumns']
    dlBase          = config['DLbase']
    dlArch          = dlBase + config['DLarch']
    dlElog          = dlBase + config['DLeLog']
    dlOpts          = config['DLOpts']
    grupeList       = config['Grupes']
    total           = 0
    failures        = 0
    # NOTE: items missing from metadata will be replaced with "?"
    ytdlFileFormat  = "/%(id)s" + sep + "%(duration)s"+ sep + ".%(ext)s"

    dlOpts['ignoreerrors'] = True              # TEMPORARY ?????
    #dlOpts['verbose'] = True                  # Useful for debugging

    # Add crucial download options. Some options MUST be added in the DL loop
    # dlOpts['force-ipv6'] = True                # May not be enabled on host
    dlOpts['writeinfojson'] = True
    dlOpts['progress_hooks'] = [callback]      # Called at least once / video
    dlOpts['download_archive'] = dlArch        # Facilitates updates w/o dupes
    dlOpts['restrictfilenames'] = True         # Required format for DLd files
    eLog = open(dlElog, mode='a+')             # Error log file for all grupes
    with youtube_dl.YoutubeDL(dlOpts) as ydl:
        for grupe in grupeList:
            if not grupeList[grupe]['Active']: continue # Skip this grupe
            SQLrows2Add = []               # Empty the list of downloads
            ErrorList = []                 # Empty the list of errors
            print("\nBEGIN " + grupe)      # Marks start of group in log

            if not os.path.isdir(dlBase + grupe):  # If it doesn't exist
                os.mkdir(dlBase + grupe)           #  create folder 4 grupe

            # Add qualifier for minimum video duration (in seconds)
            dur = grupeList[grupe]['Duration']
            if dur != None and dur > 0:
                dur = "duration > %d" % dur
                ydl.params['match_filter'] = utils.match_filter_func(dur)
            elif 'match_filter' in ydl.params.keys():
                del ydl.params['match_filter']  # No duration filter

            # Add release date range qualifier; either one or both are OK
            sd = grupeList[grupe]['Start']      # null or YYYYMMDD format
            ed = grupeList[grupe]['End']        # in JSON config file
            if sd != None or ed != None:
                dr = utils.DateRange(sd, ed)    # Dates are inclusive
                ydl.params['daterange'] = dr    # Always set a date range
            elif 'daterange' in ydl.params.keys():
                del ydl.params['daterange']     # No date filter

            # This stops downloading from playlist after this many videos
            stop = grupeList[grupe]['Stop']
            if stop != None and stop > 0: ydl.params['playlistend'] = stop
            elif 'playlistend' in ydl.params.keys():
                del ydl.params['playlistend']   # No playlist limit

            # This will change downloaded file folder for each grupe
            ydl.params['outtmpl'] = dlBase + grupe + ytdlFileFormat
            urls = grupeList[grupe]['urls']

            # Don't even try downloading videos we already have in the DB
            newUrls = filterUrls(conn, urls)

            ydl.download(newUrls)       # BEGIN DOWNLOADING!!!

            print("YOUTUBE-DL PROCESSING COMPLETE for %s" % grupe)

            # Wait for all callback threads to finish
            for th in threading.enumerate():
                if th.name != "MainThread":
                    th.join()

            # Log errors and print results of this DL grupe
            good, fails = processGrupeResults(conn, cols,
                                                len(urls), grupe, eLog)
            total += good
            failures += fails       # Accumulate totals for this run

    eLog.close()
    return total, failures

#
# Display a summary of this download session. Return them for emailing.
#
def displaySummary(conn):
    now = datetime.now().strftime("%a %b %d, %Y")
    #
    # Print the total number of files in the database
    #
    dbObj = conn.cursor().execute("SELECT COUNT(*) FROM IPFS_HASH_INDEX;")
    total  = "Total number of files downloaded and indexed: "
    total += "%5d\n" % dbObj.fetchone()[0]
    print(total)
    mail = total
    #
    # Report the number of files added in the last 30 days
    #
    strt = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    sql = "SELECT DISTINCT SUBSTR(sqlts, 6, 5) as tme, grupe, count(*) as cnt "
    sql +=  "FROM IPFS_HASH_INDEX WHERE sqlts > '" + strt + "' "
    sql += "GROUP BY grupe ORDER BY sqlts desc;"
    args = " Date   Videos   Grupe (Videos Added in the Last 30 Days)"
    mail = args + "\n"
    print(args)
    for cols in conn.execute(sql):
        args = (cols['tme'], cols['cnt'], cols['grupe'])
        mail += "%5s | %6d | %s\n" % args
        print("%5s | %6d | %s" % args)
    #
    # Print the total number of files downloaded in last 30 days
    #
    sql = "SELECT COUNT(*) FROM IPFS_HASH_INDEX WHERE sqlts > "
    dbObj = conn.cursor().execute(sql + "'" + strt + "';")
    total = " Total:  "
    total += "%5d" % dbObj.fetchone()[0]
    print(total)
    mail += total
    #
    # Report the videos downloaded today as grupes, titles & IPFS URLs
    #
    urls = ""
    sql = "SELECT grupe, title, vhash "
    sql +=  "FROM IPFS_HASH_INDEX "
    sql += "WHERE DATE(sqlts) = DATE('now', 'localtime', 'start of day');"
    rows = (conn.cursor().execute(sql)).fetchall()
    if len(rows) > 0:
        args = "\nIPFS URLs for videos downloaded today:"
        urls = args + '\n'
        print(args)
        for col in rows:
            args = (col['grupe'], col['title'][:48], col['vhash'])
            text = "%12s | %48s | https://ipfs.io/ipfs/%s" % args
            urls += text + '\n'
            print(text)

    return mail, urls


# Send a plain text message via email to recipient(s)
def emailResults(server, account, subject, origin, to, text):
    msg = EmailMessage()         # Create a text/plain container
    msg.set_content(text)
    msg['Subject'] = subject
    msg['From'] = origin
    msg['To'] = to

    context = ssl.create_default_context()
    with smtplib.SMTP(server[0], server[1]) as emailer:
        emailer.starttls(context=context)
        emailer.login(account[0], account[1])
        emailer.send_message(msg)


##############################################################################
# Get command line arguments. Returns a tuple with config and DB connection. #
# Usage: thisFile [-h] | <-c config> <-d sqlite>                             #
#                                                                            #
# Parse command line and report config info. Prints usage and exists if args #
# are invalid or missing. mff is the metadataField.json file to load         #
##############################################################################
def getCmdLineArgs():
    if len(sys.argv) >= 5:
        sqlDBfile = config = conn = None
        grupes = urls = 0

        # Required parameter: -c config file
        if sys.argv[1] == "-c" and os.path.isfile(sys.argv[2]):
            with open(sys.argv[2], 'r') as jsn:
                config = json.load(jsn)
            meta = config['DLbase'] + config['DLmeta']
            if len(meta) > 0:                   # Did config info load?
                with open(meta, 'r') as jsn:    # Now load meta fields
                    config['MetaColumns'] = json.load(jsn)['MetaColumns']
            metaSize = len(config['MetaColumns'])
            if metaSize > 0:  # All config info loaded OK?
                for grupe in config['Grupes']:  # Count groups and urls in them
                    grupes += 1
                    urls += len( config['Grupes'][grupe]['urls'] )
                print("Database Metadata Columns=%d" % metaSize)
                print("Downloaded groups will be saved in %s" % config['DLbase'])
                print("%d groups, %d urls to process" % (grupes, urls))
            else: usage()
        else: usage()

        # Required parameter: -d SQLite database file
        if sys.argv[3] == "-d":
            sqlDBfile = sys.argv[4]
            conn = openSQLiteDB(config['MetaColumns'], sqlDBfile)
            conn.row_factory = sqlite3.Row       # Results as python dictionary
        if conn == None: usage()

        # Optional parameter: -g grupe from config to use
        if len(sys.argv) >= 6 and sys.argv[5] == "-g":
            grupe = sys.argv[6]
            print(f"Ignoring all grupes in config except {grupe}")
            for grupe in config['Grupes']:       # Mark all inactive except 1
                config['Grupes'][grupe]['Active'] = false

        if not os.path.isdir(config['DLbase']):  # Create folder for results
            os.mkdir(config['DLbase'])           #  if necessary

        return config, conn, sqlDBfile           # Return essential information
    else: usage()

##############################################################################
# Primary starting point for script according to "pythonic" convention.      #
# Change this "main" the class name,  call  getCmdLine as constructor to use #
# in a proper OOP style.                                                     #
# ############################################################################
def main():
    global Config, METAFIELDS_FILE
    hash = None
    Config, conn, sqlFile = getCmdLineArgs()     # Open config, DB

    #regenerateAllGrupeIndexes(conn)             # Fix all grupe indexes
    #exit(0)

    # Command line and config file processed, time to get down to it
    good, fails = ytdlProcess(Config, conn)

    mail, urls = displaySummary(conn)
    conn.close()

    # If any downloads were successful, update IPFS with new SQLite file
    if good > 0:
        hash = publishDB(sqlFile)
        args = f"\nThe newest SQLite DB hash is: {hash}\n"
        if STATIC_DB_HASH:
            args += "It is always available at:\n"
            args += f"https://ipfs.io/ipns/{STATIC_DB_HASH}"
        mail += args
        print(args + "\n")

    # Update IPFS_INFO table in SQL DB with results for this run
    updateRunInfo(Config, sqlFile, hash, good, fails)

    if SEND_EMAIL:
        emailResults(EMAIL_SERVR, EMAIL_LOGIN,
                     EMAIL_SUB1, EMAIL_FROM, EMAIL_LIST, mail)

        if len(EMAIL_URLS) > 0 and len(urls) > 0:
            emailResults(EMAIL_SERVR, EMAIL_LOGIN,
                         EMAIL_SUB2, EMAIL_FROM, EMAIL_URLS, urls)


###############################################################################
# main is only called if this file is a script not an object class definition.#
# If this code is useful as a class it will be easy to make it one.           #
###############################################################################
if __name__ == "__main__":
    main()

exit(0)
