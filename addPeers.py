#!/usr/bin/python3
import subprocess as sp
import json
import sys

# addPeers - script to add 5 IPFS peer nodes to IPFS config file

# Usage: addPeers <config file> [restart]

# 1 = Liberty Lib, 2 = Thomas' servers and 3 = Derrick's)
PB_Peers = {
    "Peers": [
        {
            "ID": "12D3KooWSZFL4eWyufFTTfpXeKRJwkvHUq3LQ223jv6237MA1gmd",
            "Addrs": ["/ip4/104.206.255.242/tcp/4001"]
        },
        {
            "ID": "QmXf1pyCfnupeMxnyQKWsGi7z3qdJQbeiePFPCLbvUL9vn",
            "Addrs": ["/ip4/170.130.28.218/tcp/4001"]
        },
        {
            "ID": "QmbtMKVtztbZ25Yo1CX8Z8NPmHd4UK2MjnCwfKgTqMPAvX",
            "Addrs": ["/ip4/204.225.96.101/tcp/4001"]
        },
        {
            "ID": "12D3KooWDiybBBYDvEEJQmNEp1yJeTgVr6mMgxqDrm9Gi8AKeNww",
            "Addrs": ["/ip4/149.56.89.144/tcp/4001"]
        }
    ]
}


def main():
    if len(sys.argv) >= 2:
        if len(sys.argv) > 2:
            # Stop the ipfs daemon and wait for it to go away
            print("Stopping IPFS server if it's running...")
            sp.call(["/usr/bin/sudo", "/usr/bin/systemctl", "stop", "ipfs"])
            while sp.call(["/usr/bin/sudo", "/usr/bin/systemctl",
                           "is-active", "--quiet", "ipfs"]) != 3:
                pass

        with open(sys.argv[1], 'r') as file:
            config = json.load(file)

        if input:
            config["Peering"] = PB_Peers

            pretty = json.dumps(config, indent=2)
            with open(sys.argv[1], 'w') as out:
                out.write(pretty)

            if len(sys.argv) > 2:
                # Restart the ipfs daemon, wait for it to appear
                print(f"Restarting IPFS server...")
                sp.call(["/usr/bin/sudo", "/usr/bin/systemctl", "start", "ipfs"])
                while sp.call(["/usr/bin/sudo", "/usr/bin/systemctl",
                              "is-active", "--quiet", "ipfs"]) != 0:
                    pass

            count = len(PB_Peers['Peers'])
            print(f"Added {count} peers to Peering section of IPFS config file")
    else:
        print("Usage: addPeers <config file> [restart]")


###############################################################################
# main is only called if this file is a script not an object class definition.#
# If this code is useful as a class it will be easy to make it one.           #
###############################################################################
if __name__ == "__main__":
    main()

exit(0)
