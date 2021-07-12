#!/bin/bash

$(ping -c 1 1.1.1.1 > /dev/null 2>&1)
if [ $? -ne 0 ]; then
  echo "No Internet, skipping youtube-dl update"
  exit 1
fi
# Using sudo here so ipfs user can manually update
# youtube-dl with cli on demand
sudo pip3 install --upgrade youtube-dl

