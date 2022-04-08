#!/bin/bash
# This script safely shuts down the Liberty library IPFS server,
# unmounts the device and informs the user to remove it from the
# Pirate Box.

TITLE='Eject Liberty Library'
MNT_PNT=$(lsblk -o MOUNTPOINT | grep LIBERTY_LIBRARY)

if [ "$MNT_PNT" == "" ]; then
  MSG="LIBERTY_LIBRARY is not mounted!"
  zenity --info --title="$TITLE" --text="$MSG" --width=350
  exit
else
  SCRPT=$HOME/bin/libertyLibrary/removeLL.bash
  xterm -geometry 80x20+150+100 -fa 'Monospace' -fs 11 \
        -title "$TITLE" -e $SCRPT
fi
