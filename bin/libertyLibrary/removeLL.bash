#!/bin/bash
# This script safely shuts down the Liberty library IPFS server,
# unmounts the device and informs the user to remove it from the
# Pirate Box.

TITLE='Eject Liberty Library'
MNT_PNT=$(lsblk -o MOUNTPOINT | grep LIBERTY_LIBRARY)
LL_LOG=$HOME/bin/libertyLibrary/usbEvent.log
LL_IPFS=$HOME/bin/libertyLibrary/.ipfs
IPFS=$HOME/.ipfs

echo "Stopping Liberty Library IPFS server..." | tee -a $LL_LOG
sudo systemctl stop ipfs-ll > /dev/null 2>&1
# Wait for it to disappear
while : ; do
    sudo systemctl is-active --quiet ipfs-ll
    if [ $? -eq 3 ]; then break; fi
done

echo "Done. Restoring Liberty Library config from backup..." | tee -a $LL_LOG
cp $LL_IPFS/config.bak $LL_IPFS/config
if [ -e $IPFS/config ]; then
    echo "Restoring Pirate Box IPFS server configuration..." | tee -a $LL_LOG
    cp $IPFS/config.bak $IPFS/config
    echo "Restarting Pirate Box IPFS server..." | tee -a $LL_LOG
    while : ; do
        sudo systemctl is-active --quiet ipfs
        if [ $? -eq 0 ]; then break; fi
    done
    echo "Pirate Box IPFS server has restarted." | tee -a $LL_LOG
else    
    echo "Done. No Pirate Box IPFS server exists to restore!" | tee -a $LL_LOG
fi

TITLE='Eject Liberty Library'
sudo umount $MNT_PNT
if [ $? -eq 0 ]; then
    MSG="It is now safe to remove the\nLiberty Library USB device"
    echo "Liberty Library removal process is complete." | tee -a $LL_LOG
    echo "" | tee -a $LL_LOG
else
    set $(lsof $MNT_PNT | sed '1d')  # Get processes, strip column header
    M1="Failed to unmount the Liberty Library USB device!"
    MSG="$M1\n$1 PID=$2 by user $3 is one cause"
fi
zenity --info --title="$TITLE" --text="$MSG" --width=350 --height=80


