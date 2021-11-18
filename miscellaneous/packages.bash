#!/bin/bash

# NOTE: The iptables-persistent package will prompt you to save 
#       your existing firewall rules for use on startup

# Make sure we're still online
$(ping -c 1 1.1.1.1 > /dev/null 2>&1)
if [ $? -ne 0 ] || [ $(id -u) -ne 0 ]; then
  echo "You're not online and / or not running as root!"
  read -n 1 -p "Press ^C to exit" key; fi
  exit 1
fi

apt-get update -y
apt-get install -y net-tools xterm sqlite3 gparted simplescreenrecorder rpi-imager hostapd dnsmasq iptables-persistent netfilter-persistent smartmontools remmina 

pip3 install --upgrade pip
pip3 install beautifulsoup4 html5lib numpy pip-date pyperclip PySimpleGUI pyudev simplejson tinytag youtube-dl 

