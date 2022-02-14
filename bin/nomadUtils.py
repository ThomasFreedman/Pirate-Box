#!/usr/bin/python3

import os
import sys
import RNS.vendor.umsgpack as msgpack

class NomadUtils:

    def __init__(self):
        self.configdir         = os.path.expanduser("~/.nomadnetwork")

        self.configpath        = self.configdir+"/config"
        self.logfilepath       = self.configdir+"/logfile"
        self.errorfilepath     = self.configdir+"/errors"
        self.storagepath       = self.configdir+"/storage"
        self.identitypath      = self.configdir+"/storage/identity"
        self.cachepath         = self.configdir+"/storage/cache"
        self.resourcepath      = self.configdir+"/storage/resources"
        self.conversationpath  = self.configdir+"/storage/conversations"
        self.directorypath     = self.configdir+"/storage/directory"
        self.peersettingspath  = self.configdir+"/storage/peersettings"

        self.pagespath         = self.configdir+"/storage/pages"
        self.filespath         = self.configdir+"/storage/files"
        self.cachepath         = self.configdir+"/storage/cache"

        self.downloads_path    = os.path.expanduser("~/Downloads")

        # Default peer settings
        self.peer_settings = {
                "display_name": "Anonymous Peer",
                "announce_interval": None,
                "last_announce": None,
                "node_last_announce": None,
                "propagation_node": None
        }

    def save_peer_settings(self):
        file = open(self.peersettingspath, "wb")
        file.write(msgpack.packb(self.peer_settings))
        file.close()

    def set_display_name(self, display_name):
        self.peer_settings["display_name"] = display_name
        self.save_peer_settings()

# -----------------------------------------------------------------------------

def main():
    if len(sys.argv) == 2:
        nomad = NomadUtils()
        name = sys.argv[1]
        nomad.set_display_name(name)
        nomad.save_peer_settings()
    else:
        print("Usage: %s <display name>" % sys.argv[0])

                
###############################################################################
# main is only called if this file is a script not an object class definition.#
###############################################################################
if __name__ == "__main__":
    main()

exit(0)
