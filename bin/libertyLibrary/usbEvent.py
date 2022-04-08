#!/usr/bin/env python3
import subprocess as sp
import logging as lg
import pyudev
import time
import json
import sys
import os

# This is the USB event handler for Liberty Library USB storage devices.
# It starts the Liberty Library IPFS server on alternate ports so the LL
# Content is available through the main Pirate Box IPFS server node. A
# large portion of this code is used for error detection and logging. It
# always makes a backup copy of both IPFS server's config file so it can
# be restored if an error occurs. This is very important to insure the
# IPFS server's repository is not lost.

# systemd unit args: 1=action (add | remove), 2=device (/dev/sdaN),
#                    3=partition label
action = sys.argv[1]
device = sys.argv[2]
label = sys.argv[3]

PB = "/home/ipfs/"
LL = PB + "bin/libertyLibrary/"

CFG_PB = PB + ".ipfs/config"
CFG_PBBK = CFG_PB + ".bak"

CFG_LL = LL + ".ipfs/config"
CFG_LLBK = CFG_LL + ".bak"

LOG = LL + "usbEvent.log"
FMT = ["%(asctime)s %(message)s", "%m/%d/%Y %H:%M:%S"]
lg.basicConfig(filename=LOG, level=lg.INFO, format=FMT[0], datefmt=FMT[1])

# Log what brought us here
lg.info(f"{action}, {device}, {label}")

# Sections of the Liberty Library config to update so it can connect
# to the main Pirate Box IPFS server. The PeerID values will be
# added at runtime based on the values in pBox node .ipfs/config
LL_Bootstrap = ["/ip4/127.0.0.1/tcp/4001/p2p/"]
LL_Addresses = {
    "Swarm": [
      "/ip4/0.0.0.0/tcp/4010",                # Remove IPv6 addresses
      "/ip4/0.0.0.0/udp/4010/quic"
    ],
    "Announce": ["/ip4/127.0.0.1/tcp/5010"],  # Announce API port
    "NoAnnounce": [],
    "API": "/ip4/127.0.0.1/tcp/5010"
}
LL_Peers = {
    "Peers": [
        {
            "ID": "",                         # Replace with PB Peer ID 
            "Addrs": ["/ip4/127.0.0.1/tcp/4001"]
        }
    ]
}


# Logs fatal errors if any and exits, otherwise just returns
def checkOut(errs, mask):
    error = errs & mask
    if error != 0:
        lg.info(f"Fatal: error = {error}")
        exit(mask)  # Stop if any errors occurred


# Copies src to dst. Only for small files like ipfs config
def copyFile(src, dst, msg=None):
    if not msg: msg = "Making backup for"
    lg.info(f"{msg} {src}...")
    try:
        with open(src, 'r') as s, open(dst, 'w') as d:
            d.write(s.read())
    except IOError as e:
        lg.info(f"{dst}\nI/O error ({e.errno}): {e.strerror}")
        exit(-100)
    except Exception as e:  # Handle all other exceptions
        lg.info(f"{dst}\nUnexpected error: {e}")
        exit(-200)
    else:
        return


# Waits for mount point of "dev" to appear and returns it.
def getMountPoint(dev):
    out = ""
    retCode = None
    interval = 0.1
    timeout = 0.5 / interval
    while timeout > 0:
        p = sp.Popen(["grep", dev, "/proc/mounts"],
                     text=True, stdout=sp.PIPE, stderr=sp.PIPE)
        while retCode is None:
            retCode = p.poll()
            if retCode is None:
                time.sleep(interval)
                timeout -= interval
            else:
                pOut, err = p.communicate()
                if retCode == 0 and len(pOut) > 0:
                    out = pOut.split()[1]
                    return out
    return out

# Process USB "add" event for Liberty Library & start an IPFS server for it.
# Remove events are no longer handled here. They are processed by ejectLL.bash.
#
# 1. Verify the Pirate Box IPFS node has been configured (.ipfs/config exists)
#    and Liberty Library USB device has been mounted and its config exists.
#    Make copies of both IPFS server's config files as config.bak
# 2. Get PeerID of main Pirate Box IPFS server running on port 4001, 5001
# 4. Get PeerID of Liberty Library's IPFS node from the USB device it's on
# 5. Append the Liberty Library IPFS PeerID to main IPFS node's peers list
# 6. Add the main IPFS node's PeerID to .ipfs/config file for Liberty Library
# 7. Remove Gateway and fix Addresses section of Liberty Library config
# 8. Re/start both IPFS nodes, main 1st, Liberty Library 2nd
if not os.path.exists(CFG_PB):
#    No popup shows up when this script is run from uDevPython!
    title = "Liberty Library Inserted"
    msg = "Please first run the Pirate Box Setup Wizard!"
    p = sp.Popen(["zenity", "--error", f"--title={title}", f"--text={msg}",
                  "--width=350"])
    p.wait()
    lg.info(f"{CFG_PB} not found!")  # TODO: fix popup 
elif action == "add": 
    pbPeers = ""
    pbID = ""
    lLID = ""
    errs = 0b1111  # Error flag bits (4 bits)
    mountPoint = getMountPoint(device)
    if mountPoint == "":
        lg.info("Couldn't get the Liberty Library mountpoint")
        exit(-1)

    # If mounted, update the config file of the auxiliary IPFS server
    if os.path.exists(CFG_LL):
        lg.info(f"Mounted device {device} on {mountPoint}")

        copyFile(CFG_PB, CFG_PBBK)  # Make backups of both IPFS server configs
        copyFile(CFG_LL, CFG_LLBK)

        # Read the config file for the main Pirate Box IPFS server and get
        #  its' PeerID and list of Peers from it
        try:
            with open(CFG_PB, 'r') as pbCfg:
                configPB = json.load(pbCfg)
            pbID = configPB["Identity"]["PeerID"]
            pbPeers = configPB["Peering"]["Peers"]
        except IOError as e:
            lg.info(f"{CFG_PB}\nI/O error ({e.errno}): {e.strerror}")
        except JSONDecodeError as e:
            lg.info(f"{CFG_PB}\nJSON decoder error ({e.errno}): {e.strerror}")
        except Exception as e:  # Handle all other exceptions
            lg.info(f"{CFG_PB}\nUnexpected error: {e}")
        else:
            errs &= 0b1110  # Reset bit 0, no errors reading main IPFS config

        # Read the config file for the Liberty Library IPFS server
        try:
            with open(CFG_LL, 'r') as llCfg:
                configLL = json.load(llCfg)
            llID = configLL["Identity"]["PeerID"]
        except IOError as e:
            lg.info(f"{CFG_LL}\nI/O error ({e.errno}): {e.strerror}")
        except JSONDecodeError as e:
            lg.info(f"{CFG_LL}\nJSON decoder error ({e.errno}): {e.strerror}")
        except Exception as e:  # Handle all other exceptions
            lg.info(f"{CFG_LL}\nUnexpected error: {e}")
        else:
            errs &= 0b1101  # Reset bit 1, no errors reading LL config

        checkOut(errs, 0b0011)  # Stop if errors above
        lg.info(f"Adding Liberty Lib Peer (...{llID[-5:]}) to Pirate Box config")
        try:
            pbPeers.append({"ID": llID, "Addr": ["/ip4/127.0.0.1/tcp/4010"]})
            configPB["Peering"]["Peers"] = pbPeers
            pretty = json.dumps(configPB, indent=2)
            with open(CFG_PB, 'w') as out:
                out.write(pretty)
        except KeyError as e:
            lg.info(f"{CFG_PB}\nKey Error error: {e}")
        except IOError as e:
            lg.info(f"{CFG_PB}\nI/O error ({e.errno}): {e.strerror}")
        except JSONDecodeError as e:
            lg.info(f"{CFG_PB}\nJSON decoder error ({e.errno}): {e.strerror}")
        except Exception as e:  # Handle all other exceptions
            lg.info(f"{CFG_PB}\nUnexpected error: {e}")
        else:
            errs &= 0b1011  # Reset bit 2, no errors updating main IPFS config

        checkOut(errs, 0b0111)  # Stop if errors above
        lg.info(f"Adding PBox Peer ID (...{pbID[-5:]}) to Liberty Library config")
        try:
            LL_Bootstrap[0] += pbID
            LL_Peers["Peers"][0]["ID"] += pbID
            configLL["Bootstrap"] = LL_Bootstrap
            configLL["Addresses"] = LL_Addresses
            configLL["Peering"] = LL_Peers
            if "Gateway" in inconfigLL: del configLL["Gateway"]
            pretty = json.dumps(configLL, indent=2)
            with open(CFG_LL, 'w') as out:
                out.write(pretty)
        except KeyError as e:
            lg.info(f"{CFG_LL}\nUnexpected error: {e}")
        except IOError as e:
            lg.info(f"{CFG_LL}\nI/O error ({e.errno}): {e.strerror}")
        except JSONDecodeError as e:
            lg.info(f"{CFG_LL}\nJSON decoder error ({e.errno}): {e.strerror}")
        except Exception as e:  # Handle all other exceptions
            lg.info(f"{CFG_LL}\nUnexpected error: {e}")
        else:
            errs &= 0b0111  # Reset bit 3, no errors updating Liberty Lib cnfg

        checkOut(errs, 0b1000)  # Stop if errors above
        # Should add timeout checks for these subprocesses
        lg.info("Restarting Pirate Box IPFS server to add Liberty Library...")
        p = sp.Popen(["sudo", "systemctl", "start",
                      "ipfs"])
        p.wait()
        while sp.call(["sudo", "systemctl", "is-active", "--quiet",
                       "ipfs"]) != 0:
            time.sleep(0.1)

        lg.info("Done. Starting Liberty Library IPFS server...")
        p = sp.Popen(["sudo", "systemctl", "start",
                      "ipfs-ll"])
        p.wait()
        # Detection of successful LL server start needs improvement!!!
        while sp.call(["sudo", "systemctl", "is-active", "--quiet",
                       "ipfs-ll"]) != 0:
            time.sleep(0.1)
        lg.info("The Liberty Library IPFS server has started")

    else:
        lg.info(f"{CFG_LL} not found!")

