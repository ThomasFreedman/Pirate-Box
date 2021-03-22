#!/usr/bin/python3
import ipfshttpclient as api
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
        self.DLfolder = os.getenv('HOME') + '/Downloads/ipfs/'
        self.DBlist = {'Texas': 'QmWQeoj8mRKcCtveuiQ8Db9tKW4Y5u75LXQUC5ob38J2Xw',
                       'New York': 'k2k4r8kzf2pxvn73cm1nwtz57zh6e363r7m61k0ghailc0oazmwc4nox'}

    # Get the latest SQLite database from IPFS for the named server
    def getDB(self, serverName):
        hash = self.DBlist[serverName]
        save = self.DLfolder + hash + '.sqlite'
        #return Ipfs.get(self, hash, 'ipns', save)
        return save

    # Retrive a file from IPFS and save as <save> under the ipfs downloads folder.
    # If the save name is not provided the file will be named "<hash>.file"
    def get(self, hash, ipns=None, save=None):
        if save: out = save
        else: out = hash + ".file"
        if ipns: hash = '/ipns/' + hash   # Add ipNs prefix
        #self.Server.get(hash, out)
        os.system(f'ipfs get -o={out} {hash} > /dev/null 2>&1')
        return f'{out}'

    # Add a file to IPFS and return it's hash.
    def add(self, file):
        pass

    # Pin a file on this server to keep the IPFS garbage collector away form it.
    def pin(self, file):
        pass

