#!/bin/bash

# This is the ExecStart target for systemd ipfs-ll.service,
# which may go away in favor of direct launch via python's
# subprocess module.

export IPFS_PATH=/home/ipfs/bin/libertyLibrary/.ipfs
/home/ipfs/go/bin/ipfs daemon --enable-namesys-pubsub
