#!/bin/bash

IPFS_HOME="/home/ipfs/.ipfs"
IPFS_SAVE="/home/ipfs/dot_ipfs_backup"
PATH_UNIT="/etc/systemd/system/ipfs.path"
IPFS_UNIT="/etc/systemd/system/ipfs.service"

restore() {
  cat <<'END3'
This tool can only upgrade the IPFS repository located on the boot drive.

To upgrade an IPFS repository on an external drive use whatever tool you like
to duplicate the existing external drive onto a larger drive, then edit the config
file and change the StorageMax value to the new, larger size. Contact support
for more information about upgrading IPFS repositories on external drives.
END3
}

# Does the current repository reside on an external drive?
if [ -L $IPFS_HOME ]; then
  MSG1='Your IPFS repository resides on an external drive\n\n'
  MSG2='Do you wish to restore your backup repository?'
  zenity --question --text="${MSG1}${MSG2}" --width=350 --height=100
  if [ $? -ne 0 ]; then 
    zenity --info --text="$(restore)" --width=600 --height=100
    exit 1
  else 
    systemctl stop ipfs > /dev/null 2>&1 # Stop the IPFS server daemon
    rm -rf $PATH_UNIT $IPFS_HOME      # Remove path unit & symbolic link
    mv $IPFS_SAVE $IPFS_HOME          # Restore repo from backup
    mv ${IPFS_UNIT}.backup $IPFS_UNIT # Restore IPFS systemd unit
    systemctl daemon-reload
    systemctl start ipfs > /dev/null 2>&1 # Start the IPFS server daemon
    MSG="Backup repository restored,\IPFS has been restarted."
    zenity --info --text="$MSG" --width=250 --height=100
    exit 0
  fi
else
  CMD="sudo /home/ipfs/bin/addUSBdrive.bash"
  FONT="-fa 'Monospace' -fs 12"
  TITLE="Upgrade IPFS Storage"
  GEOMETRY="-geometry 60x10+150+100"
  xterm $GEOMETRY $FONT -title "$TITLE" -e "${CMD}"
fi



