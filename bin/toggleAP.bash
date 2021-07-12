#!/bin/bash

# This script toggles the static DHCP on or off for wlan0 interface
# to allow the Pi to connect normally as a WiFi client, or to enable
# it so the Pi can act as an access point and bridge to wired eth0. 
# It does by changing the symbolic link between 2 dhcpcp.conf files.
# The script uses zenity to provide an easy GUI interface you can 
# at the the main menu with alacarte. Enjoy!

DHCP=/etc/dhcpcd.conf
NOAP=${DHCP}.noAP
AP=${DHCP}.AP

# Test current state of DHCP on wlan0 interface
WIFI="#static ip_address=192.168.4.1/24"
TEST=$(grep "$WIFI" /etc/dhcpcd.conf)

if [ "$TEST" != "" ]; then
  MSG='Access Point is disabled, enable it?'
  zenity --question --text="$MSG" --width=250 --height=100
  if [ $? -eq 0 ]; then 
    MSG='Enabling AP mode of WiFi\non wlan0 after reboot'
    zenity --info --text="$MSG" --width=200 --height=100
    $(sudo rm -rf $DHCP; sudo ln -s $AP $DHCP)
  fi
else
  MSG='Access Point is enabled, disable it?'
  zenity --question --text="$MSG" --width=250 --height=100
  if [ $? -eq 0 ]; then 
    MSG='Disabling AP mode of WiFi\non wlan0 after reboot'
    zenity --info --text="$MSG" --width=200 --height=100
    $(sudo rm -rf $DHCP; sudo ln -s $NOAP $DHCP)
  fi
fi
