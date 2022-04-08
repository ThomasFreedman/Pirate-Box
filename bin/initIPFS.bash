#~/bin/bash
#
# This script will initialize IPFS and start an IPFS server instance. It runs on
# every ipfs account login and with the IPFS Setup Wizard.
#
# The initial "out of the box" settings for 1st Live boot are:
# 1) Initialize new repository with a unique peerID
# 2) Set storageMax to use 1GB of drive space
# 3) Adds 4 IPFS peer nodes (NY, TX, 2 for Derrick in Maine)
# 4) Enables the systemd unit and starts the IPFS server
# 5) Opens port 4001 for IPFS bootstrapping & peer communications
#
# Parameters used (may be empty)
# $1 == Directory for repository (can be .ipfs or any other name)
# $2 == Integer number of gigabytes for repository (storageMax value)
#
# Will initialize a 1G repository & start IPFS only on first boot of Live USB.
# Setup wizard may invoke to initialize a new repository using parameters.
#
# A log of the initialization process can be found in init.log of the repository

GOVER=1.12.17                       # Info only - version in use with this OS
HOME=/home/ipfs
LIVE=$HOME/Live-usb-storage         # Pirate Stick Only! Remainder of USB storage
REPO=$HOME/.ipfs                    # .ipfs is a symlink in $HOME folder

if [ -f $REPO/config ]; then exit 0; fi # Repository already initialized
#
# Create the .ipfs folder at appropriate location
#
if [ "$1" == "" ]; then             # No parameter, use default location
  if [ -d $LIVE ]; then             # Is this a Live USB environment?
    IPFS=$LIVE/.ipfs                # Yes, put IPFS repository on USB space
  else
    IPFS=$HOME/.ipfs_               # Installed environment, not on Live USB
  fi
else                                # Repo location was provided as parameter,
  IPFS=$1                           #   from IPFS Setup Wizard or other tool
fi
rm -rf $REPO                        # Remove old symlink
if [ ! -d $IPFS ]; then
  mkdir $IPFS                       # Create the actual IPFS repo folder
fi                                  #  if necessary, then create a
ln -s $IPFS $REPO                   #   new symlink to it in $HOME
#
# A new IPFS repository folder should now exist, so initialize it
#
ipfs init > $REPO/init.log 2>&1     # Create on $LIVE, $HOME or $1 location
#
# Verify successfully initialized
#
if ! grep -qic 'peer identity:' $REPO/init.log; then
  ERR="No peer identity found after 'ipfs init'"
  echo -e $ERR >> $REPO/init.log
  if [ "$1" == "" ]; then
    exit -1
  else            # Invocation via the IPFS Setup Wizard - report error & exit
    zenity --error --text="$ERR" --width=250
    exit -1
  fi
#
# Update storageMax, add peers, enable systemd unit, start IPFS, open port - GO!
#
else
  CONFIG=$REPO/config                   # IPFS repository configuration file
	SIZE=${2//[!0-9]/}                    # Leave only numbers, if anything
	if [ "$2" == "" ]; then SIZE=1; fi    # Nothing provided use default
	sed -i "s/^\(.*StorageMax\":\).*$/\1   \"${SIZE}G\",/g" $CONFIG
	echo "Initialized $REPO with ${SIZE}G storageMax" >> $REPO/init.log 2>&1
	$($HOME/bin/addPeers.py $CONFIG >> $REPO/init.log 2>&1)
	sudo systemctl enable ipfs >> $REPO/init.log 2>&1
	sudo systemctl start ipfs >> $REPO/init.log 2>&1;
	sudo ufw allow 4001/tcp >> $REPO/init.log 2>&1
fi

