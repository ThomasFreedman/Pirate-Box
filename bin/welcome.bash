#!/bin/bash
www=/var/www/html
apd=hotspot/config/hostapd.conf

cd /home/ipfs/bin

# This is a one-time setup for a randomized SSID for Access Point
grep "PirateBox____" $apd > /dev/null 2>&1
if [ $? -eq 0 ]; then
  newHSssid=PirateBox$((1 + $RANDOM % 9999))
  sed -i -e "/^ssid=/c\ssid=$newHSssid" $apd
  sed -i -e "/^wpa_passphrase=/c\wpa_passphrase=@RRRsp0t" $apd
  sudo cp $apd /etc/hostapd/.

  # If PBIP8 is installed, update docs under web server
  if [ -f ${www}/pbox-ssid.html ]; then
    sed -i "s/inactive/$newHSssid/" ${www}/pbox-ssid.html
    h="href='pbox-ssid.html'"
    t="title='SSID: "$newHSssid"'"
    sed -i "s/<\!--ssid-->/<a $h $t>Pirate Box Hotspot<\/a>/" ${www}/index.html
  fi
fi

if [ -f welcome.off ]; then exit; fi

TITLE='Welcome!'
MSG='The welcome screen is now disabled.'
zenity --filename="welcome.txt" --text-info --title="$TITLE" --width=520 --height=400
if [ $? -ne 0 ]; then
  zenity --question --text="Stop showing this at startup?" --width=150 --height=100
  if [ $? -eq 0 ]; then
    zenity --title="Disabling Welcome..." --info --text="$MSG" --width=280 --height=100
    touch welcome.off
    exit
  fi
fi



