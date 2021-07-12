#!/usr/bin/python3
from nonblock import nonblock_read
import ipfshttpclient as api
import PySimpleGUI as sg
import subprocess as sp
import inspect
import time
import os

# Class to interface with IPFS

class Ipfs:

    # NOTE: 3-16-2021 - ipfshttpclient does not yet support daemon 0.8.0
    #                   so for now will use shell to interface with ipfs

    def __init__(self):
        # Some way to obtain decentralized metadata databases to populate
        # this dictionary needs to be developed.  The dictionary keys are
        # the values that appear in the Config menu.  The values are IPnS
        # addresses published by each server that describe their content.
        #self.Server = api.connect()  # to: /dns/localhost/tcp/5001/http
        self.DBcacheTime = 24       # Max age in hours of database cache
        self.MaxWaitTime = 60       # Max time to wait for IPFS commands
        self.DLfolder = os.getenv('HOME') + '/Downloads/ipfs/'
        self.DBlist = {
            'Texas (IPFS)':
                'QmWQeoj8mRKcCtveuiQ8Db9tKW4Y5u75LXQUC5ob38J2Xw',
            'New York (IPFS)':
                'k2k4r8kzf2pxvn73cm1nwtz57zh6e363r7m61k0ghailc0oazmwc4nox',
            'PBVG Database':
                'pbvg',
            'Liberty Library on USB':
                'llbry.sqlite'
        }

    # Get latest SQLite database from IPFS for the named server or use cache
    def getDB(self, serverName, gui, x, y):
        hash = self.DBlist[serverName]
        cache = self.DLfolder + hash
        if not serverName.endswith("USB"):        # USB DB - Liberty Library?
            cache += '.sqlite'
            stat = os.stat(cache)
            age = (time.time() - stat.st_mtime) / 3600 # Cache age in hrs
            if age > self.DBcacheTime:            # If old, ask user to refresh
                msg = f"Update metadata for {serverName}?"
                a = sg.popup_yes_no(msg, no_titlebar=True,
                                    location=(x + 450, y + 100),
                                    background_color="#3E3E30",
                                    grab_anywhere=True)
                if a == "Yes":
                    dt = time.strftime("_%Y%m%d_%H:%M:%S",
                                       time.gmtime(stat.st_ctime))
                    os.rename(cache, cache + dt)
                    if not Ipfs.get(self, hash, gui, x, y, 'ipns', cache):
                        sg.popup("Oh no!", "A problem occured while",
                                 f"updating the metadata from {serverName}!",
                                 "Reverting to the previous metadata.",
                                 no_titlebar=True, location=(x + 450, y + 100),
                                 background_color="#602020", grab_anywhere=True)
                        os.rename(cache + dt, cache)
        return cache


    # Retrieve a file from IPFS and save as <save> under the Downloads/ipfs.
    # If the save name is not provided the file will be named "<hash>.file".
    # Show progress and display any errors in popup windows.
    def get(self, hash, gui, x, y, ipns=None, save=None):
        if save: out = save
        else: out = hash + ".file"
        if ipns: hash = '/ipns/' + hash   # Add ipNs prefix
        #self.Server.get(hash, out)
        args = [f"ipfs", "get", f"-o={out}", f"{hash}"]

        # Use command line for now to run the IPFS command
        try:
            p = sp.Popen(args, shell = False,
                         stdout=sp.PIPE, stderr=sp.STDOUT)
        except Exception as e:
            sg.popup("Aw shucks, something went wrong...",
                     inspect.stack()[1][3] + ' error: ' + str(e),
                     location=(locX + 300, locY - 100))
            return False
                
        output = ""
        result = False
        progress = 0
        timer = self.MaxWaitTime
        pop = gui.progressWindow("open", x, y, 0, timer) # Show progress popup
        while True:
            getOut = nonblock_read(p.stdout)       # Get output if any
            if getOut is None:                     # Subprocess closed stream
                p.wait()
                if "100.00%" in output:            # Success?
                    result = True
                break                              # Yep! We're done here
            elif len(getOut) > 0:
                output += str(getOut)              # Accumulate output
                progress += 1
            else:
                time.sleep(1)                      # Wait a bit
                timer -= 1
                if timer < 1: break
            gui.progressWindow(pop, x, y, progress, timer) # Decr timer

        gui.progressWindow(pop, 0, 0, -1, 0)       # Close the progress popup
        return result
    

    # Add a file to IPFS and return it's hash.
    # At least for now this will be handled by webui in browser
    def add(self, file):
        pass


    # Pin a file on this server to keep the IPFS garbage collector away from it.
    # The timeLimit parameter sets the maxmum amount of time to wait for the pin
    # command to complete (default set above). Returns True on success False
    # otherwise. No: displays progress bar & timer at bottom of result window.
    # 4 SOME ODD REASON result window freezes, so switched to popup progressBar.
    def pin(self, gui, hash, timeLimit):
        if timeLimit is None: timer = self.MaxWaitTime
        else: timer = timeLimit
        max = timer
        #self.Server.pin(hash)
        try:                       ### Added shell == False...
            p = sp.Popen([f"ipfs", "pin", "add", f"{hash}"],
                         shell = False, stdout=sp.PIPE, stderr=sp.STDOUT)
        except Exception as e:
            sg.popup("Aw shucks, something went wrong...",
                     inspect.stack()[1][3] + ' error: ' + str(e))
            return False
                
        output = ""
        result = None
        progress = 0
        pop = gui.progressWindow("open", 400, 200, 0, timer) # Show progress popup
        while True:
            pinOut = nonblock_read(p.stdout)   # Get output if any available
            if pinOut is None:                 # Subprocess closed stream
                p.wait()
                if f"pinned {hash}" in output: # Pinned successfully?
                    result = True
                else: result = False
                break                          # We're done here
            elif len(pinOut) > 0:
                output += str(pinOut)
                progress += 1
 #               resWin['-PROG-'].update(current_count=progress, max=max)
            else:
                time.sleep(1)
                timer -= 1
#                minutes, s = divmod(timer, 60)
#                h, m = divmod(minutes, 60)                
                if timer < 1: break
#                else: resWin['-TIMR-'].update("%02d:%02d:%02d" % (h, m, s))                
            gui.progressWindow(pop, 0, 0, progress, timer) # Decr timer

        gui.progressWindow(pop, 0, 0, -1, 0)   # Close the progress popup
        return result
