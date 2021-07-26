#~/bin/bash
# This script safely shuts down the Liberty library IPFS server,
# unmounts the device and informs the user to remove it from the
# Pirate Box.
#

# Stop the Liberty library IPFS server via systemd unit
sudo systemctl stop ipfs-ll > /dev/null 2>&1

# Wait for it to disappear
while : ; do
    sudo systemctl is-active --quiet ipfs-ll
    if [ $? -eq 3 ]; then break; fi
done

MNT_PNT=$(lsblk -o MOUNTPOINT | grep LIBERTY_LIBRARY)
TITLE='Eject Liberty Library'
sudo umount $MNT_PNT
if [ $? -eq 0 ]; then
    MSG='It is now safe to remove the\nLiberty Library USB device'
else
    MSG='Please wait!\nFailed to unmount the\nLiberty Library USB device'
fi
zenity --info --title="$TITLE" --text="$MSG" --width=280 --height=80


