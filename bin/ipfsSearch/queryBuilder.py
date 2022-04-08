#!/usr/bin/python3
import PySimpleGUI as sg
import vlcPlaylist as pl
import guiLayouts as gl
import sqlDB
import json
import ipfs
import os

# GUI layouts and Event Processing for PBox Search

class pBoxQuery:


    def __init__(self):
        self.Pwd = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.Ipfs = ipfs.Ipfs()
        self.Vlc = pl.Playlist()
        self.Sql = sqlDB.sql(self.Ipfs)
        self.Gui = gl.pBoxGUI(self.Ipfs)
        self.Day6 = ''          # Need to persist date and time b/c can't read value of text field
        self.Tmv6 = ''
        self.Display = []
        self.Where = {'Clause': [], 'Show': []}
        self.Grupes = []
        self.Ext = []
        self.ExKey = []
        self.TITLE = None       # Set at run time to number of last column (title) in results
        self.Format = []
        self.SaveFolder = "/home/ipfs/Documents"
        self.Settings = {'server': None, "cacheLife": None, 'saveFolder': None}

        # Metadata fields in SQLite DB available to use as search criteria.
        # Each field (column in SQLite) is categorized under an input state.
        # These names define those states for each field to select the right
        # widget to obtain user input for that field. TODO: implement code
        # for ComboBox, Radio and CheckBox input types.

        # These are the query builder states as the filter criteria is selected.
        self.Start     = 0      # Starting state where users select a field
        self.ListBox   = 1      # Select value(s) from a list (like Start state)
        self.TextBox   = 2      # any; if int > < =, starts with ends with contains, exact...
        self.ComboBox  = 3      # Choice from a list or can type in items not in list
        self.Radio     = 4      # Choose 1 of n
        self.CheckBox  = 5      # Choose any / all of n
        self.Calendar  = 6      # Date and optional time in SQLite3 format: 'YYYYMMDD HH:MM:SS'
        self.NumSlide  = 7      # Linear slider to select a numeric value or type one in
        self.Time      = 8      # Returns number of seconds. Displayed as HH:MM:SS
        self.MultiText = 9      # Similar to TextBox but with different radio buttons

        #
        # CONSIDER LOADING THE FOLLOWING FROM A JSON CONFIG FILE
        #
        # This list of database fields is searched against the keywords or phrases for state9
        self.MultiFields = [
            "grupe", "_filename", "album", "title", "fulltitle", "alt_title", "artist", "categories_0",
            "creator", "description", "extractor", "format", "license", "webpage_url_basename"
        ]
        # This dictionary maps Search Criteria to DB metadata fields which
        # correspond to input states (which are synonymous with input widget).
        # This would need to be defined by the metadata publisher
        self.SearchCriteria = {
            "MULTI FIELD SEARCH": ["ALL", self.MultiText],
            "Item #": ["pky", self.NumSlide],
            "Title": ["title", self.TextBox],
            "Publisher": ["grupe", self.ListBox],
            "Publish Date": ["upload_date", self.Calendar],
            "Source": ["extractor_key", self.ListBox],
            "Description": ["description", self.TextBox],
            "Length": ["duration", self.Time],
            "Views": ["view_count", self.NumSlide],
            "Likes": ["like_count", self.NumSlide],
            "Dislikes": ["dislike_count", self.NumSlide],
            "Avg. Rating": ["average_rating", self.NumSlide],
            "ID": ["id", self.TextBox],
            "Type": ["ext", self.ListBox],
            "Size": ["vsize", self.NumSlide],
            "Width": ["width", self.NumSlide],
            "Height": ["height", self.NumSlide],
            "Format": ["format_note", self.ListBox],
            "IPFS CID":  ["vhash", self.TextBox],
            "IPFS Date": ["sqlts", self.Calendar],
            "IPFS File": ["_filename", self.TextBox],
            "User meta text": ["abr", self.TextBox],
            "User meta date": ["abr", self.Calendar],
            "User meta list": ["abr", self.ListBox],
            "User meta time": ["abr", self.Time],
            "User meta radio": ["abr", self.Radio],
            "User meta number": ["abr", self.NumSlide],
            "User meta combo box": ["abr", self.ComboBox],
            "User meta check boxes": ["abr", self.CheckBox]
        }

    # Save any settings that need to persist for next app start
    def saveSettings(self, file):
        self.Settings['cacheLife']  = self.Ipfs.DBcacheTime    # Current value in use
        self.Settings['maxWaitTime']  = self.Ipfs.MaxWaitTime  # Current value in use
        self.Settings['saveFolder'] = self.SaveFolder          # Where results were last saved
        with open(file, 'w') as cfg:
            json.dump(self.Settings, cfg)

    # Restore the settings saved last
    def restoreSettings(self, file):
        try:
            with open(file, 'r') as jsn:
                self.Settings = json.load(jsn)
                self.Ipfs.DBcacheTime = self.Settings['cacheLife']
                self.Ipfs.MaxWaitTime = self.Settings['maxWaitTime']
                self.SaveFolder = self.Settings['saveFolder']
                self.serverOpen(self.Settings['server'], 200, 100)
        except:
            pass  # Use default values if problem with settings file

    # Open the chosen SQLite database file, initialize lists and display popup of DB stats
    def serverOpen(self, server, x ,y):
        self.Sql.openDatabase(server, self.Gui, x, y)
        if self.Sql.Conn: 
            # Get selections for multi-select items (radio buttons, checkboxes, listboxes & comboboxes
            grpSql = "select distinct grupe from IPFS_HASH_INDEX ORDER BY grupe;"
            self.Grupes = self.Sql.getListFromSql(grpSql)
            extSql = "select distinct ext from IPFS_HASH_INDEX where ext not like '%unknown%';"
            self.Ext = self.Sql.getListFromSql(extSql)
            exKSql = "select distinct extractor_key from IPFS_HASH_INDEX where extractor_key not like '%unknown%';"
            self.ExKey = self.Sql.getListFromSql(exKSql)
            fmtSql = "select distinct format_note from IPFS_HASH_INDEX where format_note not like '%unknown%';"
            self.Format = self.Sql.getListFromSql(fmtSql)

            # Not sure of best way to present multiselect elements whose selections come from the DB
            self.LBox = self.SearchCriteria

            self.Gui.AppWin['-META-'].update(values=list(self.SearchCriteria.keys()), disabled=False)
        else:
            self.Gui.AppWin['-META-'].update(values=[], disabled=False)
            msg = f"\nAn Error Occurred opening {server}!\n\nPlease try again later."
            sg.popup(msg)


    def resetAll(self):
        state = pBoxQuery.resetToState0(self)
        self.Where = {'Clause': [], 'Show': []}             # Clear search criteria lists
        self.Gui.AppWin['-META-'].update(values=[])         # Clear metadata select list
        self.Gui.AppWin['-META-'].update(disabled=True)     # Disable it too
        if self.Gui.ResultWin: self.Gui.ResultWin.close()
        self.Gui.AppWin['-TODO-'].update(values=[])         # Clear search criteria list
        self.Gui.AppWin['-SEARCH-'].update(disabled=True)   # Disable buttons
        self.Gui.AppWin['-CLEAR-'].update(disabled=True)
        return state

    # Clear search results, close input windows and return to state 0 to select other criteria
    def resetToState0(self):
        self.Gui.AppWin['-META-'].Widget.selection_clear(0, len(self.SearchCriteria)) # Remove selection
        self.Gui.AppWin['-META-'].update(scroll_to_index=0)                       # Scroll to top
        if len(self.Gui.InputWidget) > 0: 
            self.Gui.resetWidget().close()                                        # Close input window
            self.Gui.InputWidget = []
        if self.Gui.ResultWin:
            self.Gui.ResultWin.close()                                            # Close this too?
            self.Gui.AppWin['-DEL-'].update(disabled=True)
        return 0


    # Run the search query using the criteria in the Where[Clause] list. Title must be last in
    # select list. The x and y parameters are where the result window is opened on the desktop.
    # Display results in fixed size fields so appearance is in columns.  Export results can be
    # split on whitespace and title must be last, so title words can be joined into 1 column.
    def doSearch(self, x, y):
        result = []
        query = "SELECT pky, upload_date, ext, CAST(vsize as FLOAT) / 1000000000 as size, "
        query +=        "CAST(duration as int) as dur, title from IPFS_HASH_INDEX WHERE "
        if len(self.Where['Clause']) == 0:
            query += " 1=1 limit 50"
        else:
            for clause in self.Where['Clause']:
                query += clause
        rows = self.Sql.runQuery(query)
        items = len(rows)
        if len(rows) > 0:
            result = ['  KEY  PUBLISHED  TYPE    SIZE    LENGTH  TITLE']
            self.TITLE = 5  # Index of title data in results; need for export
            for r in rows:
                # Strip unicode characters Tcl doesn't like and handle nulls
                cols = list(range(len(r)))
                for col in range(len(r)):  # for each column in the row
                    if r[col] is not None:
                        vLst = str(r[col])
                        vLst = [vLst[i] for i in range(len(vLst)) if ord(vLst[i]) in range(65536)]
                        cols[col] = ''
                        for char in vLst: cols[col] += char
                        if cols[col].startswith('unknown'): cols[col] = '?'
                    else: cols[col] = '?'  # Replace nulls (None values)

                # Add hyphens to make date easier to read
                if len(cols[1]) > 1: d = f"{cols[1][0:4]}-{cols[1][4:6]}-{cols[1][6:8]}"  # YYYY-MM-DD format
                else: d = '?'

                # Truncate sizes less than 10MB
                if len(cols[3]) > 1: s = "%5s" % str(cols[3])[0:4]
                else: s = '?'

                result.append("%5s %10s %5s  %5sg  %5ssec  %s" %
                              (cols[0], d, cols[2], s, cols[4], cols[5]))

        else: result.append("No results found based on your search criteria")
        self.Gui.ResultWin = sg.Window('Search Results', self.Gui.queryResults(),
                                       location=(x, y), modal=True, force_toplevel=True,
                                       keep_on_top=False, disable_close=True, finalize=True)

        self.Gui.ResultWin['-ROWS-'].update(f"{items} items")
        vhash = "vhash is prefixed as first column for csv and txt exports."
        qry = [self.Sql.Sever + " where"] + self.Gui.AppWin['-TODO-'].get_list_values()
#        qry = [self.Sql.Sever + " where"] + [query]
        self.Gui.ResultWin['-RESULTS-'].metadata = [vhash, "Query: "] + qry
        self.Gui.ResultWin['-RESULTS-'].update(values=result)
        self.Gui.ResultWin['-PROG-'].update(current_count=0, visible=False)

    # Save results to a file of the selected type, csv, text or VLC playlist
    def saveResults(self, file, type):
        dataOut = []
        search = self.Gui.ResultWin['-RESULTS-'].metadata

        # Split lines into columns
        for i in self.Gui.ResultWin['-RESULTS-'].get_indexes():
            item = self.Gui.ResultWin['-RESULTS-'].get_list_values()[i]
            dataOut.append(item.split(maxsplit=self.TITLE)) # Don't split title

        if type == 'xspf':
            for row in dataOut:    # Write result rows out to file
                key = row[0]       # Get pky to lookup hash for URL
                dur = row[4][:-3]  # Remove the "sec" units string
                title = row[5]     # Get the title for this item
                if not key.isdecimal() or int(key) < 1 or not dur.isdecimal():
                    continue
                hash = self.Sql.getHash(key)
                if not hash.startswith("Qm") or len(hash) != 46: continue
                url = f"http://127.0.0.1:8080/ipfs/{hash}"
                dur = str(int(dur) * 1000)        # Fix duration for vlc
                self.Vlc.add_track(url, dur, title)
            self.Vlc.save_playlist(file)

        elif type == 'txt':
            with open(file, 'w') as txt:
                line = " ".join(search)
                txt.write(line + '\n')
                for row in dataOut:             # Write result rows out to file
                    key = row[0]  # Get pky to lookup hash
                    if not key.isdecimal() or int(key) < 1:
                        continue
                    txt.write(" ".join([self.Sql.getHash(key)] + row) + '\n')

        # I've tried many variations of code but can't get rid of weird " chars
        elif type == 'csv':
            with open(file, 'w') as csv:
                line = ""
                for item in search:             # Write query parameters to file
                    item.replace('"', '')       # Remove double quotes from data
                    line += f'"{item}",'
                line = line[:-1] + "\n"         # Replace last comma with a newline
                csv.write(line)
                for row in dataOut:             # Write result rows out to file
                    key = row[0]                # Get pky to lookup hash
                    if not key.isdecimal() or int(key) < 1:
                        continue
                    line = f'"{self.Sql.getHash(key)}",'  # vhash as first column
                    for col in row:
                        col.replace('"', '')    # Remove double quotes from data
                        line += f'"{col}",'     # Double quote all values
                    line = line[:-1] + "\n"     # Replace last comma with a newline
                    csv.write(line)


    # Pin each item selected in the result window one by one
    # TODO: Resolve problem with progress / timer at bottom of result window:
    #       it should display timer and progress bar on a single row.
    #       Removed the timer text element to "resolve" the issue.
    def pinSelected(self, x, y):
        todo = list(self.Gui.ResultWin['-RESULTS-'].get_indexes())
        bad = []
        progress = 0
        max = len(todo)
        self.Gui.ResultWin['-PROG-'].update(current_count=0, visible=True, max=max)
        for idx in todo:
            item = self.Gui.ResultWin['-RESULTS-'].get_list_values()[idx]
            key = item.split(maxsplit=1)[0]  # We need the key to lookup hash to pin
            if not key.isdecimal() or int(key) < 1:
                max -= 1                     # Skip header row or invalid keys
                continue
            hash = self.Sql.getHash(key)
            if not hash.startswith("Qm") or len(hash) != 46: continue
            if not self.Ipfs.pin(self.Gui, hash, None):
                bad.append(idx)
            progress +=1
            self.Gui.ResultWin['-PROG-'].update(current_count=progress, visible=True, max=max)

        self.Gui.ResultWin['-RESULTS-'].update(set_to_index=bad)
        msg = "Pinning Complete!"
        if bad: msg += f"\nPinning failed for the {len(bad)} highlighted items"
        sg.popup(msg)
        self.Gui.ResultWin['-PROG-'].update(current_count=0, visible=False, max=max)


    # Process input collected from user and create SQL where clause for it.
    # The equivalent "Show" list is what is shown to the user. Everything is
    # derived from the user criteria name thru the SearchCriteria dictionary:
    # KEY = criteria label, [0] == db field, [1] == state / input widget.
    def addSQL2SearchCriteriaList(self, criteria, input):
        self.Gui.AppWin['-SEARCH-'].update(disabled=False)
        self.Gui.AppWin['-CLEAR-'].update(disabled=False)

        field, state = self.SearchCriteria[criteria]   # Get DB field & state 
        if len(self.Where['Clause']) > 0: clause = ' and '
        else: clause = ''
        show = clause

        # Process selections from a list
        if state == self.ListBox:
            choices = len(input['list'])
            if choices > 0:
                c = 0
                clause += f"{field} in ("
                show += f"{criteria} is "
                for choice in input['list']:
                    clause += f"'{choice}'"
                    show += choice
                    c += 1
                    if c < choices:
                        clause += ','
                        show += ' or '
                clause += ')'

        # Process text input
        elif state == self.TextBox:
            if input['equ']:
                clause += f"{field} = {input['text']}"
                show += f"{criteria} = '{input['text']}'"
            elif input['has']:
                clause += f"{field} like '%{input['text']}%'"
                show += f"{criteria} contains '{input['text']}'"
            elif input['str']:
                clause += f"{field} like '{input['text']}%'"
                show += f"{criteria} starts with '{input['text']}'"
            elif input['end']:
                clause += f"{field} like '%{input['text']}%'"
                show += f"{criteria} ends with '{input['text']}'"

        # TODO: Figure out how to handle items whose selections come from DB
        elif state == self.ComboBox:
            pass
        elif state == self.Radio:
            pass
        elif state == self.CheckBox:
            pass

        # Process Date and optional time input
        elif state == self.Calendar:
            if input['max']: mnx = '<='
            elif input['min']: mnx = '>='
            else: mnx = '='
            dateTime = input['datetm']
            clause += f"{field} {mnx} '{dateTime.replace('-', '')}'"
            show += f"{criteria} {mnx} {dateTime}"

        # Process numeric input
        elif state == self.NumSlide:
            if input['max']: mnx = '<='
            elif input['min']: mnx = '>='
            else: mnx = '='
            clause += f"CAST({field} as int) {mnx} {input['number']}"
            show += f"{criteria} {mnx} {input['number']}"

        # Process time input
        elif state == self.Time:
            if input['min']: mnx = '>='
            else: mnx = '<='
            clause += f"CAST({field} as int) {mnx} {input['seconds']}"
            show += f"{criteria} {mnx} {input['seconds']} seconds"

        # Process multi-text input
        elif state == self.MultiText:
            if input['has']:
                words = input['text'].split()
                for field in self.MultiFields:
                    for word in words:
                        clause += f"{field} like '%{word}%' or "
                clause += "0=1"
                show += f"{criteria} matches any word: {input['text'].replace(' ', ', ')}"
            elif input['all']:
                for field in self.MultiFields:
                    clause += f"{field} like '%{input['text']}%' or "
                clause += "0=1"
                show += f"{criteria} matches phrase: '{input['text']}'"

        self.Where['Clause'].append(clause)
        self.Where['Show'].append(show)
        self.Gui.AppWin['-TODO-'].update(values=self.Where['Show'])



# ----------- Widget EVENT PROCESSING methods ----------- #
    # These methods process events generated from the gui layouts.
    def handleState1(self, event, values):
        if event == '-LBOX1-':
            self.Gui.InputWidget[0]['Ok1-'].update(disabled=False)
            if values and len(values) > 0:
                return {'list': values['-LBOX1-']}

    def handleState2(self, event, values):
        txtInput = None
        if event in ('-TXT2-','-HAS2-','-STR2-','-END2-','-EQU2-'):
            if event in ('-TXT2-'):
                txtInput = str(values['-TXT2-'])
                self.Gui.InputWidget[0]['-HAS2-'].update(disabled=False)
                self.Gui.InputWidget[0]['-STR2-'].update(disabled=False)
                self.Gui.InputWidget[0]['-END2-'].update(disabled=False)
                self.Gui.InputWidget[0]['Ok2-'].update(disabled=False)
            if txtInput is not None and len(txtInput) > 0:
                self.Txt2 = txtInput
                return {'text': self.Txt2, 'has': values['-HAS2-'], 'str': values['-STR2-'],
                        'end': values['-END2-'], 'equ': values['-EQU2-']}

    def handleState3(self, event, values):
        pass

    def handleState4(self, event, values):
        pass

    def handleState5(self, event, values):
        pass

    def handleState6(self, event, values):
        if event in ('Calendar','-SLD6-','-TMV6-','-MIN6-','-MAX6-','-EQU6-'):
            if event == 'Calendar':
                self.Gui.InputWidget[0]['-DAT6-'].update("")
                self.Gui.InputWidget[0]['-SLD6-'].update(disabled=True)
                d = sg.popup_get_date(no_titlebar=False)
                if d is not None:
                    date = "%d-%02d-%02d " % (d[2], d[0], d[1])
                    self.Day6 = date  # These 2 values need to be persistent
                    self.Tmv6 = ''    # Reset time when a new date is selected
                    self.Gui.InputWidget[0]['-TMV6-'].update(self.Tmv6, disabled=False)
                    self.Gui.InputWidget[0]['-TMV6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['Ok6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-SLD6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-MAX6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-MIN6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-EQU6-'].update(disabled=False)

            if event == '-SLD6-':
                slider = int(values['-SLD6-'])
                if slider > 0:
                    minutes, s = divmod(slider, 60)
                    h, m = divmod(minutes, 60)
                    self.Tmv6 = "%02d:%02d:%02d" % (h, m, s)
                else:
                    self.Tmv6 = ""
                self.Gui.InputWidget[0]['-TMV6-'].update(self.Tmv6)
            elif event == '-TMV6-':
                t = values['-TMV6-'].split(':')
                if len(t) == 3 and t[0].isdecimal() and \
                        t[1].isdecimal() and t[2].isdecimal():
                    h = int(t[0]) % 24
                    m = int(t[1]) % 60
                    s = int(t[2]) % 60
                    self.Tmv6 = "%02d:%02d:%02d" % (h, m, s)
                else:  self.Tmv6 = ""

            if len(self.Day6) > 0:
                date = "%s %s" % (self.Day6, self.Tmv6)
                self.Gui.InputWidget[0]['-DAT6-'].update(date)
                return {'datetm': date.rstrip(), 'min': values['-MIN6-'],
                        'max': values['-MAX6-'], 'equ': values['-EQU6-']}

    # Get a numeric value. If a number is entered into the input box,
    # update the slider with that value. Max value allowed is set in self.Max7
    def handleState7(self, event, values):
        if event in ('-SLD7-', '-NUM7-','-MIN7-','-MAX7-','-EQU7-'):
            numInput = 0
            if event == '-SLD7-':
                numInput = int(values['-SLD7-'])
                self.Gui.InputWidget[0]['-NUM7-'].update(numInput)
            elif event == '-NUM7-':
                numInput = str(values['-NUM7-'])[0:7]
                if numInput.isdecimal():
                    numInput = int(numInput)
                    self.Gui.InputWidget[0]['-SLD7-'].update(numInput)
                else:
                    numInput = 0
                    self.Gui.InputWidget[0]['-NUM7-'].update(numInput)

            self.Gui.InputWidget[0]['-NUM7-'].update(numInput)
            self.Gui.InputWidget[0]['Ok7-'].update(disabled=False)
            return {'number': numInput, 'min': values['-MIN7-'], 'max': values['-MAX7-'], 'equ': values['-EQU7-']}

    # Update the text element with time as hrs, mins, secs string,
    # and slider input to value in seconds. If a number is entered
    # into the input box, update the slider with that value.
    def handleState8(self, event, values):
        if event in ('-SLD8-', '-SEC8-', '-MIN8-', '-MAX8-'):
            self.Gui.InputWidget[0]['-SLD8-'].update(disabled=False)
            secInput = None
            if event == '-SLD8-':
                secInput = int(values['-SLD8-'])
                self.Gui.InputWidget[0]['-SEC8-'].update(secInput)          # Update text input to match
            elif event == '-SEC8-':
                secInput = str(values['-SEC8-'])[0:5]
                if secInput.isdecimal():
                    secInput = int(secInput)
                    self.Gui.InputWidget[0]['-SLD8-'].update(secInput)      # Update slider imput to match
                else:
                    secInput = 0
                    self.Gui.InputWidget[0]['-SEC8-'].update(secInput)

            # Update the time text element based on slider or text input
            if secInput is not None:
                minutes, s = divmod(secInput, 60)
                h, m = divmod(minutes, 60)
                self.Gui.InputWidget[0]['-TIM8-'].update("%02d:%02d:%02d" % (h, m, s))
                self.Gui.InputWidget[0]['Ok8-'].update(disabled=False)
                return {'seconds': secInput, 'min': values['-MIN8-'], 'max': values['-MAX8-']}

    def handleState9(self, event, values):
        txtInput = None
        if event in ('-TXT9-','-HAS9-','-ALL9-'):
            if event in ('-TXT9-'):
                txtInput = str(values['-TXT9-'])
                self.Gui.InputWidget[0]['-HAS9-'].update(disabled=False)
                self.Gui.InputWidget[0]['-ALL9-'].update(disabled=False)
                self.Gui.InputWidget[0]['Ok9-'].update(disabled=False)
            if txtInput is not None and len(txtInput) > 0:
                self.Txt9 = txtInput
                return {'text': self.Txt9, 'has': values['-HAS9-'], 'all': values['-ALL9-']}

