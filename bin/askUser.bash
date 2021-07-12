#!/bin/bash

if [ `./getPeerID.bash` == "1" ]; then
  MSG='IPFS is already initialized,\ndelete the repository\nand re-initialize?'
  zenity --question --text="$MSG" --width=250 --height=100
  if [ $? -ne 0 ]; then exit 1; fi
  systemctl disable ipfs
  systemctl stop ipfs
  while true; do                      # verify stopped
    systemctl is-active --quiet ipfs
    if [ $? -ne 0 ]; then break; fi
  done
fi

# Get minimum required info from user for basic operation
TITLE='Set the hostname'
MSG='Give your new Pirate Box a name.\n(a-Z 0-9 . - only, 253 chars max):'
INP=`zenity --entry --title="$TITLE" --text="$MSG" --width=250 --height=100`
if [ ${#INP} -gt 253 ]; then
  zenity --error --text="Too many characters!"
else
  echo $INP > /etc/hostname
  echo 127.0.0.1 $INP localhost >> /etc/hosts
fi

# Calculate disk space to use for IPFS
BYTES=1
GBYTE=1000000000
DEFAULT_MAX=50
TITLE='Set IPFS StorageMax'
TOTAL=`df --output=avail -B 1 /home | tail -n 1` # Free space in bytes on home partition
TOTAL=`expr $TOTAL - ${GBYTE}`                   # Reserve 1G for op sys
GB=`expr $TOTAL / ${GBYTE}`
MSG="Free space is aprx. ${GB}GB. Enter a % (1-100%)\nto use for IPFS (default = 50%):"
INP=`zenity --entry --title="$TITLE" --text="$MSG" --width=320 --height=100`
if [ $? -ne 0 ]; then
  INP=$DEFAULT_MAX
else
  INP=${INP//[!0-9]/}  # Only numbers please
  if [ "$INP" == "" ] || [ "$INP" -lt 10 ] || [ "$INP" -gt 100 ]; then
    zenity --error --text="Invalid entry, using 50%" --width=200 --height=100
    INP=$DEFAULT_MAX
  fi
fi
UNITS=$GBYTE
export MAX=`expr $(( $TOTAL*${INP}/100 )) / $UNITS`
zenity --info --text="Setting IPFS StorageMax to ${MAX}GB" --width=200 --height=100
printf -v STORAGE_MAX "%dG" $MAX     # The default StorageMax parameter value

# Have user change the ipfs account password
xterm -geometry 55x5+225+150 -fa 'Monospace' -fs 12 -title "Change Your Password" -e ./getPassw.bash ipfs
MSG="Great! It's time to start\nyour IPFS node. Click\nOK when you're ready"
zenity --info --text="$MSG" --width=200 --height=80

#
# Inputs collected, time to initialize...
#
TITLE='Starting IPFS...'
xterm -geometry 80x20+150+100 -fa 'Monospace' -fs 12 -title "$TITLE" -e ./initializeIPFS.bash
