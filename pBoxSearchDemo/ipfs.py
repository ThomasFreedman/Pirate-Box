#!/usr/bin/python3
import ipfshttpclient as api
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

        # WHAT? Why can't I access instance values within methods here?
        # Some how there are 2 instances of this object in play????????
        self.DBcacheTime = 24       # Max age in hours of database cache
        self.DLfolder = os.getenv('HOME') + '/Downloads/ipfs/'
        self.DBlist = {
            'Texas (IPFS)':
                'QmWQeoj8mRKcCtveuiQ8Db9tKW4Y5u75LXQUC5ob38J2Xw',
            'New York (IPFS)':
                'k2k4r8kzf2pxvn73cm1nwtz57zh6e363r7m61k0ghailc0oazmwc4nox',
            'Liberty Library (local)':
                'LIBERTY_LIBRARY'
        }

    # Get latest SQLite database from IPFS for the named server or use cache
    def getDB(self, serverName, sg, x, y):
        hash = self.DBlist[serverName]
        cache = self.DLfolder + hash + '.sqlite'
        if not serverName.endswith("(local)"):    # Local DB - Liberty Library?
            stat = os.stat(cache)
            age = int((time.time() - stat.st_ctime) / 3600) # Cache age in hrs
            if age > self.DBcacheTime:            # If old, ask user to refresh
                msg = f"Update metadata for {serverName}?"
                a = sg.popup_yes_no(msg, no_titlebar=True,
                                    location=(x + 450, y + 100),
                                    background_color="#3E3E30",
                                    grab_anywhere=True)
                if a == "Yes":
                    dt = time.strftime("%Y%m%d_%H:%M:%S",
                                       time.gmtime(stat.st_ctime))
                    os.rename(cache, cache + dt)
                    # TODO: check result, restore cache on error
                    return Ipfs.get(self, hash, 'ipns', cache)
        return cache

    # Retrieve a file from IPFS and save as <save> under the Downloads/ipfs.
    # If the save name is not provided the file will be named "<hash>.file"
    def get(self, hash, ipns=None, save=None):
        if save: out = save
        else: out = hash + ".file"
        if ipns: hash = '/ipns/' + hash   # Add ipNs prefix
        #self.Server.get(hash, out)
        os.system(f'ipfs get -o={out} {hash} > /dev/null 2>&1')
        return f'{out}'

    # Add a file to IPFS and return it's hash.
    # At least for now this will be handled by webui in browser
    def add(self, file):
        pass

    # Pin a file on this server to keep the IPFS garbage collector away from it.
    # Can we make use of --progress option using subprocess module instead of
    # os.system?
    def pin(self, hash):
        #self.Server.pin(hash)
#        time.sleep(2)
        out = os.system(f'ipfs pin add {hash} > /dev/null 2>&1')
        return out
