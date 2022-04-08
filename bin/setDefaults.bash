#!/bin/bash
www=/var/www/html
hst=/etc/hosts
etc=/etc/hostapd/hostapd.conf
hot=$HOME/bin/hotspot/config/hostapd.conf
nom=$HOME/.nomadnetwork/config
idx=$HOME/.nomadnetwork/storage/pages/index.mu
peer=$HOME/.nomadnetwork/storage/peersettings

nhp='Hello! This is the index.mu for ID on nomad network'

cd $HOME/bin

# This script sets various defaults such as the SSID for the
# WiFi hotspot and Nomadnet node name for Reticulum network,
# and keeps various files under the webserver updated.

# Get the current number from the default hotspot SSID or
# generate one if no hotspot SSID has been set.  Set both
# num and ssid.  ssid will always be valid but num may be
# empty if default has been replaced by user supplied val
num=$(sed -n "s/ssid=PirateBox\([0-9]\+\|_\{4\}\)/\1/p" $hot)
if [ "$num" == "____" ]; then   # 1st section is 1 time only
  num=$((1 + $RANDOM % 9999))   # Generate a hotspot SSID
  ssid="PirateBox$num"
  sudo hostnamectl set-hostname "${ssid}"
  sudo bash -c "echo -e \"127.0.0.1\t${ssid}\" >> $hst"
  sed -i -e "/^wpa_passphrase=/c\wpa_passphrase=@RRRsp0t" $hot
  sed -i -e "/^ssid=/c\ssid=$ssid" $hot
elif [ "$num" == "" ]; then
  ssid=$(sed -n "s/^ssid=\(.*\)$/\1/p" $hot) # Provided by user
else
  ssid="PirateBox$num"          # Default already set
fi

#
# Make sure all of the ssid values are consistent
#
sed -i -e "/^ssid=/c\ssid=$ssid" $hot      # (re)Set hotspot ssid to use
sudo cp $hot $etc > /dev/null 2>&1         # Set daemon process config
sed -i "s/\( is:\)\(.*\)<\/p>/\1 $ssid<\/p>/" ${www}/pbox-ssid.html
h="href='pbox-ssid.html'"
t="title='hotspot SSID: "$ssid"'"
o="for <a $h .*\/a>"
sed -i "s/<\!--ssid-->\|$o/for <a $h $t>Pirate Box $num<\/a>/" ${www}/index.html

# Set the default nomandnet client's node and peer names if they're not set.
# If empty set it to the hotspot SSID value, and to index.mu.
nam=$(sed -n "s/node_name *= *\(.*\)/\1/p" $nom > /dev/null 2>&1)
if [ -f $nom ] && [ "$nam" == "" ]; then
  sed -i "s/\(node_name *=\)\(.*\)/\1 $ssid/" $nom > /dev/null 2>&1
  echo ${nhp/ ID / $ssid } > $idx
fi
if grep -q 'Anonymous Peer' $peer ; then
  nomadUtils.py set-name $ssid
fi

# Create a default IPFS server with 1GB of storage
$HOME/bin/initIPFS.bash
