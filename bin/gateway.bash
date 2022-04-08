#!/bin/bash

CMD=/home/ipfs/bin/openCloseGate.py
CFG=/home/ipfs/.ipfs/config

# Ask user if they want to open or close the gateway
TITLE='Public Gateway'
MSG='Give other computers access to your gateway?'

zenity --question --text="$MSG" --ok-label="YES" --cancel-label="NO" --width=250 --height=100

if [ $? -ne 0 ]; then 
   WHAT=close
else
   WHAT=open
fi

eval "$CMD $WHAT $CFG"
