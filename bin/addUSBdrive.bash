#!/bin/bash

VOL_LABEL="IPFS_USB_REPO"
REPO_BASE="/media/ipfs/$VOL_LABEL"
REPO_HOME="$REPO_BASE/.ipfs"
IPFS_HOME="/home/ipfs/.ipfs"
IPFS_SAVE="/home/ipfs/dot_ipfs_backup"
IPFS_CONF="$REPO_HOME/config"
PATH_UNIT="/etc/systemd/system/ipfs.path"
IPFS_UNIT="/etc/systemd/system/ipfs.service"

DETECTOR="lsblk -n -o NAME,SIZE,TYPE /dev/sd*"

intro() {
  cat <<'END1'
This tool will format an external usb drive (or partition on it) and copy the 
current IPFS repository (/home/ipfs/.ipfs) to it, saving a backup in a new
folder named /home/ipfs/dot_ipfs_backup. The tool will ask how much space you 
wish to use for IPFS storage on the external drive (the default is 100%) and 
update the IPFS configuration to match. 

Mounting of the external USB repository at system boot is handled by the Linux 
uDev system automatically, however this tool must update the ipfs.service to wait
for the drive to be ready before IPFS can be started. After successfully running
this tool the external USB drive must be plugged in when your Pirate Box is booted
or IPFS will not work.

If you wish to customize the format of the external usb drive, you must create it 
before you start this tool using gparted or another tool of your choice. Please 
note that only Linux formats (ext2, ext3 and ext4) are acceptable filesystems for
the IPFS repository. 

IF THE DRIVE YOU WISH TO ADD IS ALREADY PLUGGED IN, REMOVE IT NOW AND THEN CLICK OK
END1
}

insertUSB() {
  cat <<'END2'
Now plug in the USB device you want to add. 

Automounting of volumes may occur on some external 
USB devices. If so you must wait for automounting 
to complete before you click OK. You may dismiss
any windows that appear as volumes are automounted. 

Please be patient. There are many variations of USB 
devices this tool must handle, and the size of the
existing repository to be copied is also a factor.
END2
}

pathFile() {  # Systemd path unit file that sets dependency on USB repo
  cat <<'END4'
[Unit]
Description=Defines required path for ipfs.service unit

[Path]
PathExists=/media/ipfs/IPFS_USB_REPO/.ipfs
Unit=ipfs.service

[Install]
WantedBy=multi-user.target
END4
}

ipfsFile() {  # ipfs.service unit file with updated restart rate limits
  cat <<'END5'
[Unit]
Description=IPFS daemon

[Service]
User=ipfs
Group=ipfs
Environment="IPFS_PATH=/home/ipfs/.ipfs"
ExecStart=/home/ipfs/go/bin/ipfs daemon --enable-namesys-pubsub
Restart=on-failure
RestartSec=30s
StartLimitBurst=4
StartLimitIntervalSec=120

[Install]
WantedBy=multi-user.target
END5
}

# Determine the external USB drive and any partitions it may have
zenity --info --text="$(intro)" --width=620 --height=200
$DETECTOR 1>/tmp/sdOut 2>/dev/null
zenity --info --text="$(insertUSB)" --width=420 --height=100
$DETECTOR 1>/tmp/sdIn 2>/dev/null

# Get the difference which is inserted USB device and partitions on it
delta=$(diff /tmp/sdOut /tmp/sdIn | tr -d \> | grep sd)
drive=(${delta})

i=0
n=0
# Create a list of device options including all partitions
while [ $i -lt ${#drive[@]} ]
do
  if [[ ${drive[$i]} =~ ^sd ]]; then
    options[n]="${drive[$i]} ${drive[$i+1]} ${drive[$i+2]}"
    n=$(($n+1)) # Bump options index / counter
  fi
  i=$(($i+3))   # Bump to next index of drive array
done

title="USB Drive Information"
prompt="Choose entire disk or a partition, then OK or Cancel to exit"
# Present the drive information to the user in a list to select from
while choice=$(zenity --list --title="$title" --width 300 --height 300 \
               --text="$prompt" --column="Available Options:" "${options[@]}");
do
  selected=""
  if [[ "$choice" =~ ^sd ]]; then  # All viable choices will start with "sd"
    selected=$choice
    break
  else
    exit
  fi
done

# Confirm the choice of which device or partition to use
MSG1="Are you sure you want to use\n$selected?\n\n"
MSG2="THIS WILL ERASE ALL DATA on \n$selected"
zenity --question --text="${MSG1}${MSG2}" --width=250 --height=100
if [ $? -ne 0 ]; then 
  zenity --info --text="Cancelled" --width=100 --height=100
  exit 1; 
fi

# Inform user of operations we do in terminal window
echo "Reformating USB device $selected..."

# Split selection into dev array (device, size and type)
IFS=" " 
read -r -a dev <<< "$selected"
chosen="/dev/${dev[0]}"   # Selected device or partition
baseDv="/dev/${dev:0:3}"  # Base device, no partition #

# Unmount all automounted partitions of selected drive
umount "${baseDv}"?* > /dev/null 2>&1  # This can be tricky, watchout!

# For a partition, just use mkfs.ext4 to reformat it:
if [ "${dev[2]}" == "part" ]; then
  # Use double -F to force format if already formatted 
  mkfs.ext4 -F -F -q -L $VOL_LABEL $chosen > /dev/null 2>&1
else  # Entire disk
  wipefs -af $baseDv > /dev/null 2>&1    # Start with a clean slate
  # Now create a new partition table with 1 partition for entire disk
  echo 'type=83' | sfdisk $baseDv > /dev/null 2>&1
  chosen="${baseDv}1"   # Change chosen whole device to partition
  # This forces formatting of the new partition and sets the label
  mkfs.ext4 -F -F -q -L $VOL_LABEL $chosen > /dev/null 2>&1
fi
# These lines useful for adding an entry to /etc/fstab -- UNUSED --
# I'll use systemd and path unit instead to enforce USB dependency
#blkInfo=($(blkid /dev/sda1))
#uuid=${blkInfo[2]//[\"]/}

#
# The new device is formatted and ready for mounting & use
#
echo "Waiting for automounting on $REPO_BASE..."

# It must be unplugged then plugged back in for uDev to automount it.
MSG1="Please remove the USB drive and\n"
MSG2="re-insert it for automounting.\n\n"
MSG3="Click OK after you plug it in..."
zenity --info --text="$MSG1$MSG2$MSG3" --width=250 --height=100

systemctl stop ipfs > /dev/null 2>&1 # Stop the IPFS server daemon

while [ ! -d $REPO_BASE ]; 
do 
  sleep 2            # Wait for system to mount it
done

# Rename the existing repository to create a backup
echo "Creating a backup of your existing repository..."
mv $IPFS_HOME $IPFS_SAVE > /dev/null 2>&1

# Now copy the old repository to the external USB drive
echo "Copying the existing repository to $selected..."
cp -aR $IPFS_SAVE $REPO_HOME > /dev/null 2>&1

# Create a symbolic link to the external repository
echo "Creating a symbolic link to repository on $selected..."
ln -s $REPO_HOME $IPFS_HOME > /dev/null 2>&1

# Ask user for amount of space to use on new drive for IPFS
MSG="Enter the IPFS StorageMax value in GB, up to ${dev[1]}:"
INP=`zenity --entry --title="$TITLE" --text="$MSG" --width=320 --height=100`
if [ $? -ne 0 ]; then       # Cancel clicked,
  INP=${dev[1]}             #  so use the entire disk
else                        # Validate the value the user input
  MAX=${dev[1]:0:-1}        # Max drive space number minus the 'G'
  INP="${INP//[!0-9|\.]/}"  # Leave only numbers and decimal point
  # Check for invalid inputs
  if [ "$INP" == "" ] || (( $(echo "$INP < 1" | bc) )) || (( $(echo "$INP > $MAX" | bc) )); then   
    zenity --error --text="Invalid entry!" --width=200 --height=100
    INP=${dev[1]}           # Set StorageMax to size of drive or partition
  else
    INP="${INP}G"           # Add the 'G' to numeric value user entered
  fi
fi

# Update the ipfs config file on USB
echo "Setting the IPFS StorageMax value to to ${INP}..."
sed -i "s/^\s*\"StorageMax.*$/    ~StorageMax~: ~${INP}~,/g" $IPFS_CONF
sed -i "s/~/\"/g" $IPFS_CONF

# Make a backup of systemd service unit in case we need to revert changes later
echo "Making a backup of the IPFS systemd unit..."
cp -a $IPFS_UNIT ${IPFS_UNIT}.backup

# Install new systemd units
echo "$(pathFile)" > $PATH_UNIT
echo "$(ipfsFile)" > $IPFS_UNIT
systemctl daemon-reload  > /dev/null 2>&1

# Restart ipfs.service
echo "Restarting the IPFS server with new USB repository..."
systemctl start ipfs > /dev/null 2>&1

# Done! 
zenity --info --text="IPFS Storage Upgraded to ${INP}!" --width=200 --height=100
