#!/bin/bash

VOL_LABEL="IPFS_USB_REPO"
HOME_DOWN="/home/ipfs/Downloads"
HOME_YTDL="/home/ipfs/bin/videoGrabber/ytDL"
REPO_BASE="/media/ipfs/$VOL_LABEL"
REPO_HOME="$REPO_BASE/.ipfs"
REPO_DOWN="$REPO_BASE/Downloads"
REPO_YTDL="$REPO_BASE/Downloads/ytDL"
IPFS_HOME="/home/ipfs/.ipfs"
IPFS_SAVE="/home/ipfs/dot_ipfs_backup"
IPFS_CONF="$REPO_HOME/config"
PATH_UNIT="/etc/systemd/system/ipfs.path"
IPFS_UNIT="/etc/systemd/system/ipfs.service"

DETECTOR="lsblk -n -o NAME,SIZE,TYPE /dev/sd*"

intro() {
  cat <<'END1'
This will format an external usb device (or partition on it) and copy the
current IPFS repository to it. You will be asked how much space you want
to use on the device for IPFS storage. Use custom formatting for devices
larger than 4 terabytes (4T). See information panel after clicking OK.

IF THE DRIVE YOU WISH TO ADD IS ALREADY PLUGGED IN,
REMOVE IT NOW AND THEN CLICK OK
END1
}

moreInfo() {
  cat <<'INF1'
All of your current IPFS files in /home/ipfs/.ipfs will be saved
in a new folder named /home/ipfs/dot_ipfs_backup which this tool
can restore after this upgrade is complete. The space you ask for
on the new USB device will be used to update the new IPFS config-
uration but will not apply to the original, saved copy.

Mounting of the external USB repository at system boot is handled
by the Linux uDev system automatically, however this tool must
update the ipfs.service to wait for the drive to be ready before
IPFS can be started.

After this upgrade the external USB drive must be plugged in when
your Pirate Box is booted or IPFS will not work.

If you wish to customize the format of the external usb drive,
you must create it before you start this tool using gparted, fdisk
or another tool of your choice. Please note that only Linux ext2,
ext3 and ext4 filesystem types are acceptable for the IPFS
repository. If you need more than 4 terabytes, you will need to
custom format your device using a GPT partition table, not MBR, and
select a partition, not the whole device when you use this tool.

This tool will only repartition an entire device with a single
partition 4TB or less, or use the space of an existing partition
which could be more than 4TB if the partition table is GPT.

INF1
}

insertUSB() {
  cat <<'END2'
Now plug in the USB device you want to add.

Automounting of volumes may occur on some external USB devices. If so you
must wait for automounting to complete before you click OK. You may dismiss
any windows that appear as volumes are automounted.

Please be patient. There are many variations of USB devices this tool must
handle, and the size of the existing repository to be copied is also a factor
for how long this upgrade will take.
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
zenity --info --text="$(intro)" --width=550
MSG="Would you like more information?"
zenity --question --text="${MSG}" --width=250
if [ $? -eq 0 ]; then
  zenity --info --text="$(moreInfo)" --width=500
fi

$DETECTOR 1>/tmp/sdOut 2>/dev/null
NOSD=$(cat /tmp/sdOut | grep -e "^sd*")  # Filter non-primary items
zenity --info --text="$(insertUSB)" --width=600
$DETECTOR 1>/tmp/sdIn 2>/dev/null
SDIN=$(cat /tmp/sdIn | grep -e "^sd*")   # Filter non-primary items

# Get the difference which is inserted USB device and partitions on it
delta=$(diff <(echo "$NOSD") <(echo "$SDIN") | tr -d \>)
#delta=$(diff <(echo $NOSD) <(echo $SDIN) | tr -d \>)
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
prompt="Choose a disk or a partition, then OK or Cancel to exit"
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
zenity --question --text="${MSG1}${MSG2}" --width=250
if [ $? -ne 0 ]; then
  zenity --info --text="Cancelled"
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
  if [ $? -ne 0 ]; then
    zenity --info --text="Error: the partition failed to format!" --width=300
    exit 1;
  fi
else  # Entire disk
  wipefs -af $baseDv > /dev/null 2>&1    # Start with a clean slate
  # Now create a new partition table with 1 partition for entire disk
  echo 'type=83' | sfdisk $baseDv > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    zenity --info --text="Error: partitioning the device!" --width=250
    exit 1;
  fi
  chosen="${baseDv}1"   # Change chosen whole device to partition
  # This forces formatting of the new partition and sets the label
  mkfs.ext4 -F -F -q -L $VOL_LABEL $chosen > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    zenity --info --text="Error: the device failed to format!" --width=250
    exit 1;
  fi
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
MSG2="re-insert it after 10 - 20 seconds\n"
MSG3="for the automounter to detect it.\n\n"
MSG4="Click OK after you plug it back in..."
zenity --info --text="$MSG1$MSG2$MSG3$MSG4" --width=250

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
#
# Also migrate the Downloads & PBVG files to external USB
#
# Copy the Downloads folder to the external USB drive
echo "Copying the Downloads folder to $selected..."
cp -aR $HOME_DOWN $REPO_BASE > /dev/null 2>&1

# Now rename the Downloads folder to create a backup
echo "Creating a backup of your existing Downloads..."
mv $HOME_DOWN ${HOME_DOWN}.backup > /dev/null 2>&1

# Create a symbolic link to the copy on external USB
echo "Creating a symbolic link to Downloads on $selected..."
ln -s $REPO_DOWN $HOME_DOWN > /dev/null 2>&1

# Do the same for PBVG / ytDL files
echo "Copying the folder used for saving PBVG files to $selected..."
cp -aR $HOME_YTDL $HOME_DOWN > /dev/null 2>&1

# Rename the ytDL folder to create a backup
echo "Creating a backup of your existing ytDL folder..."
mv $HOME_YTDL ${HOME_YTDL}.backup > /dev/null 2>&1

# Create a symbolic link to the external repository
echo "Creating a symbolic link to ytDL folder on $selected..."
ln -s $REPO_YTDL $HOME_YTDL > /dev/null 2>&1
#
# Migration and backup of folders to USB device is now complete 
#

# Normalize drive/partition size in megabytes
SIZ=${dev[1]:0:-1}                        # Max drive size number
UNT=${dev[1]: -1}                         # Size units: M, G or T
if [ "$UNT" == "M" ]; then MX=1; fi       # No conversion required
if [ "$UNT" == "G" ]; then MX=1000; fi    # Convert GB to MB
if [ "$UNT" == "T" ]; then MX=1000000; fi # Convert TB to MB
MAX=$(echo "$MX * $SIZ" | bc)             # MAX == size in megabytes

# Ask user for amount of space to use on new drive for IPFS
MSG="Enter IPFS StorageMax as a whole % (1-100) of ${MAX}MB"
INP=`zenity --entry --title="$TITLE" --text="$MSG" --width=330`
if [ $? -ne 0 ] || [ "$INP" == "100" ] || [ "$INP" == "100%" ]; then
  INP="$MAX"                # Cancel or 100 or 100% entered, use MAX
else                        # Validate the value provided by user
  INP="${INP//[!0-9]/}"     # Strip all but numbers

  # Check for invalid inputs: not empty, > 0, < 100
  if [ "$INP" == "" ] || (( $(echo "$INP < 1" | bc) )) || (( $(echo "$INP > 99" | bc) )); then
    zenity --error --text="Invalid entry!\n\nUsing 100%" --width=200
    INP="$MAX"              # on error use entire space
  else
    INP=$(echo ".$INP * $MAX" | bc)  # User provided value less than 100%
  fi
fi

# Update the ipfs config file on USB
echo "Setting the IPFS StorageMax value to to ${INP}MB..."
sed -i "s/^\s*\"StorageMax.*$/    ~StorageMax~: ~${INP}MB~,/g" $IPFS_CONF
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
GB=$(echo "$INP / 1000" | bc)          # Gigabyte units
TB=$(echo "$GB  / 1000" | bc)          # Terabyte units
if [ $GB -eq 0 ]; then GB="< 1"; fi    # bc can't do fractions
if [ $TB -eq 0 ]; then TB="< 1"; fi
MSG="IPFS Storage Upgraded to ${INP}MB! (${GB}GB, ${TB}TB)"
zenity --info --no-markup --text="$MSG" --width=200
