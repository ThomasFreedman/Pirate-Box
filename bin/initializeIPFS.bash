#~/bin/bash
# This script will initialize IPFS software and establish initial settings.
#

GOVER=1.12.17               # Info only - version in use in this SD image
REPO=/home/ipfs/.ipfs
CONFIG=$REPO/config         # IPFS repository configuration file

# Make sure we're still online
$(ping -c 1 1.1.1.1 > /dev/null 2>&1)
if [ $? -ne 0 ] || [ $(id -u) -ne 0 ]; then
  echo "You're not online!"
  echo "Press ^C to exit"
  sleep 3600
  exit 1
fi

if [ ! -d /home/ipfs/.ipfs/ ]; then
  mkdir /home/ipfs/.ipfs/; chown ipfs.ipfs /home/ipfs/.ipfs/
elif [ -L /home/ipfs/.ipfs ]; then
  MSG='Your .ipfs folder links to a\nLIBERTY LIBRARY!\nAborting IPFS setup'
  zenity --info --title="$TITLE" --text="$MSG" --width=280 --height=80
  exit
fi

rm -rf /home/ipfs/.ipfs/*  # Start from a blank slate; use explicit path here!
echo "Initializing your new IPFS node, please be patient..."
runuser -l ipfs -c "ipfs init > $REPO/init.log 2>&1"   # Initialize IPFS and log output
if [ $(./getPeerID.bash) != "1" ]; then
  zenity --error --title="Something went wrong" --text="No peer identity found!" --width=250 --height=100
  exit
fi

echo "Adding default peers..."
$(./addPeers.py $CONFIG > /dev/null 2>&1)

echo "Reserving ${MAX}GB for IPFS storage..."
sed -i "s/^\s*\"StorageMax.*$/    ~StorageMax~: ~${MAX}G~,/g" $CONFIG
sed -i "s/~/\"/g" $CONFIG

# echo "Opening required firewall ports and starting IPFS..."
ufw allow 4001/tcp > /dev/null 2>&1
ufw allow 22/tcp   > /dev/null 2>&1 # ssh

systemctl enable ipfs > /dev/null 2>&1
systemctl start ipfs > /dev/null 2>&1

cat $REPO/init.log
README=$(grep -oP '^\s+ipfs cat /ipfs/\K\S+' $REPO/init.log)
echo "in a terminal window, or enter the URL ipfs://$README in the Chromium web browser."
TITLE='Setup is complete!'
MSG='Your IPFS node is ready now.\nClick OK to close these windows'
zenity --info --title="$TITLE" --text="$MSG" --width=280 --height=80
