#!/bin/bash

IPFS_HOME="/home/ipfs/.ipfs"
HOME_DOWN="/home/ipfs/Downloads"
HOME_YTDL="/home/ipfs/bin/videoGrabber/ytDL"
IPFS_SAVE="/home/ipfs/dot_ipfs_backup"
PATH_UNIT="/etc/systemd/system/ipfs.path"
IPFS_UNIT="/etc/systemd/system/ipfs.service"

restore() {
  cat <<'END3'
This tool can only migrate data from the boot drive to an external USB device.

To upgrade an external drive to a larger one, use whatever tool you like to
duplicate the existing external drive onto a larger drive, then edit the IPFS
config file and change the StorageMax value to the new, larger size. Contact 
support for more information about upgrading IPFS repositories or external 
drives.
END3
}

# Does the current repository reside on an external drive?
if [ -L $IPFS_HOME ]; then
  MSG1='Your IPFS repository resides on an external drive\n\n'
  MSG2='Do you wish to restore from the backups saved?'
  zenity --question --text="${MSG1}${MSG2}" --width=350 --height=100
  if [ $? -ne 0 ]; then
    zenity --info --text="$(restore)" --width=600 --height=100
    exit 1
  else
    sudo systemctl stop ipfs > /dev/null 2>&1 # Stop the IPFS server
    sudo rm -rf $PATH_UNIT $IPFS_HOME         # Remove path unit & sym link
    mv $IPFS_SAVE $IPFS_HOME                  # Restore repo from backup
    sudo mv ${IPFS_UNIT}.backup $IPFS_UNIT    # Restore IPFS systemd unit
    sudo rm -rf $HOME_DOWN $HOME_YTDL         # Remove sym links
    mv ${HOME_DOWN}.backup $HOME_DOWN         # Restore Downloads folder
    mv ${HOME_YTDL}.backup $HOME_YTDL         # Restore ytDL folder
    sudo systemctl daemon-reload
    sudo systemctl start ipfs > /dev/null 2>&1 # Start the IPFS server
    MSG="Backups restored,\nIPFS has been restarted."
    zenity --info --text="$MSG" --width=250 --height=100
    exit 0
  fi
else
  CMD="sudo /home/ipfs/bin/addUSBdrive.bash"
  FONT="-fa 'Monospace' -fs 12"
  TITLE="Upgrade IPFS Storage"
  GEOMETRY="-geometry 72x16+150+100"
  xterm $GEOMETRY $FONT -title "$TITLE" -e "${CMD}"
fi



