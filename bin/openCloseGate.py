#!/usr/bin/python3
import subprocess as sp
import json
import sys

# openCloseGate - script to open or close gateway in IPFS config file
# Usage: openGateway <open|close> <config file>

gatewayC = "/ip4/127.0.0.1/tcp/8080"
gatewayO = "/ip4/0.0.0.0/tcp/8080"

headersC = {
    "Access-Control-Allow-Headers": [
        "X-Requested-With",
        "Range",
        "User-Agent"
    ],
    "Access-Control-Allow-Methods": [
        "GET"
    ],
    "Access-Control-Allow-Origin": [
        "*"
    ]
}

headersO = {
    "Access-Control-Allow-Headers": [
        "X-Requested-With",
        "Access-Control-Expose-Headers",
        "Range",
        "User-Agent"
    ],
    "Access-Control-Expose-Headers": [
        "Location",
        "Ipfs-Hash"
    ],
    "Access-Control-Allow-Methods": [
        "POST",
        "GET"
    ],
    "Access-Control-Allow-Origin": [
        "*"
    ],
    "X-Special-Header": [
        "Access-Control-Expose-Headers: Ipfs-Hash"
    ]
}


def main():
    if len(sys.argv) == 3:
        msg = sys.argv[1]
        if msg == 'open':
            gate = gatewayO
            head = headersO
        else:
            gate = gatewayC
            head = headersC
            msg += 'd'

        # Stop the ipfs daemon and wait for it to go away
        print("Stopping IPFS server if it's running...")
        sp.call(["/usr/bin/sudo", "/usr/bin/systemctl", "stop", "ipfs"])
        while sp.call(["/usr/bin/sudo", "/usr/bin/systemctl",
                      "is-active", "--quiet", "ipfs"]) != 3:
            pass

        with open(sys.argv[2], 'r') as file:
            input = json.load(file)

        if input:
            input["Addresses"]["Gateway"] = gate
            input["Gateway"]["HTTPHeaders"] = head

            pretty = json.dumps(input, indent=2)
            with open(sys.argv[2], 'w') as out:
                out.write(pretty)

            # Restart the ipfs daemon, wait for it to appear
            print(f"Restarting IPFS server with gateway {msg}...")
            sp.call(["/usr/bin/sudo", "/usr/bin/systemctl", "start", "ipfs"])
            while sp.call(["/usr/bin/sudo", "/usr/bin/systemctl",
                          "is-active", "--quiet", "ipfs"]) != 0:
                pass

            id = input["Identity"]["PeerID"]
            print(f"Gateway is now {msg} for PeerID {id}")
    else:
        print("Usage: openCloseGate <open|close><config file>")


###############################################################################
# main is only called if this file is a script not an object class definition.#
# If this code is useful as a class it will be easy to make it one.           #
###############################################################################
if __name__ == "__main__":
    main()

exit(0)
