#!/usr/bin/python3

import os
import sys
import RNS
from nomadnet import Directory
import RNS.vendor.umsgpack as msgpack

class NomadUtils:

    def __init__(self):
        self.configdir         = os.path.expanduser("~/.nomadnetwork")

        self.configpath        = self.configdir+"/config"
        self.logfilepath       = self.configdir+"/logfile"
        self.errorfilepath     = self.configdir+"/errors"
        self.storagepath      = self.configdir+"/storage"
        self.identitypath     = self.configdir+"/storage/identity"
        self.cachepath        = self.configdir+"/storage/cache"
        self.resourcepath     = self.configdir+"/storage/resources"
        self.conversationpath = self.configdir+"/storage/conversations"
        self.directorypath    = self.configdir+"/storage/directory"
        self.peersettingspath = self.configdir+"/storage/peersettings"

        self.pagespath        = self.configdir+"/storage/pages"
        self.filespath         = self.configdir+"/storage/files"
        self.cachepath        = self.configdir+"/storage/cache"

        self.downloads_path   = os.path.expanduser("~/Downloads")
        
        self.trust            = { 0x00: "WARNING", 0x01: "UNTRUSTED", 
                                  0x02: "UNKNOWN", 0xFF: "TRUSTED" }
        self.propMode         = { 0x01: "DIRECT", 0x02: "PROPAGATED" }


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

    def list_directory(self):
        nodes = Directory(self).known_nodes()
        for node in nodes:         
            name = node.display_name
            host = node.hosts_node
            addr = RNS.prettyhexrep(node.source_hash)
            trust = self.trust[node.trust_level]
            dLvry = self.propMode[node.preferred_delivery]
            
            print(f"Name: {name}\nSource: {addr}")
            print(f"Trust: {trust}\nNode host: {host}")
            print(f"Pref. Delivery: {dLvry}\n")

# -----------------------------------------------------------------------------

def main():
    nomad = NomadUtils()
    if len(sys.argv) == 2 and sys.argv[1] == "list-dir":
        nomad.list_directory()

    elif len(sys.argv) == 3 and sys.argv[1] == "set-name":
        nomad.set_display_name(sys.argv[2])
        nomad.save_peer_settings()

    else:
        print("Usage: %s list-dir | set-name <display name>" % sys.argv[0])

                
###############################################################################
# main is only called if this file is a script not an object class definition.#
###############################################################################
if __name__ == "__main__":
    main()

exit(0)
