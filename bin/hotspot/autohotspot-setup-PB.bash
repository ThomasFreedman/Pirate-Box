#!/bin/bash

# This is a new front end to the RaspberryConnect.com "Autohotspot" script,
# the bulk of which can be found in the "dispatch" script file. All of the
# user functionality is preserved, and a new help menu entry is provided
# to describe each menu item in detail via a zenity popup dialog.

# Additional changes for Pirate Box
# The default hotspot SSID name is now PirateBox with a different random
# number appended the first time the Pirate Box is booted.

# dispatch version PB-0.72.1 (23 Jul 2021), based on autohotspot-setup,
# version 0.72 (17 Oct 2020) by RaspberryConnect.com.

go()
{
 cpath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
 if [ "$1" == "HLP" ]; then
    TITLE='Pirate Box Hotspot Help'
    zenity --filename="$cpath/ReadMe.txt" --text-info --title="$TITLE" \
           --width=600 --height=400
 else
    TITLE='Hotspot Control'
    xterm -geometry 80x20+150+100 -fa 'Monospace' -fs 11 -title "$TITLE" \
       -e "sudo $cpath/dispatch.bash $1"
 fi
}

menu()
{
#selection menu
title="Pirate Box Autohotspot"
error="Invalid option, click 'OK' to choose again"
prompt="Pick an option then click OK or Cancel to exit:"
options=("1 - Automatic hotspot with Internet for connected devices"
         "2 - Hotspot for Pirate Box only, no Internet for devices"
         "3 - Permanent Hotspot with Internet for devices"
         "4 - Use normal Raspberry Pi wired & wireless networking"
         "5 - Add/Change WiFi SSID to access the Internet"
         "6 - Force to a Hotspot or Force to Network if SSID in Range"
         "7 - Change the Hotspots SSID and Password"
         "8 - Help for each of these options")

while opt=$(zenity --list --title="$title" --width 460 --height 350 \
            --text="$prompt" --column="Available Options:" "${options[@]}"); 
do
    selected=""
    case "$opt" in
    "${options[0]}" ) selected="AHN";;
    "${options[1]}" ) selected="AHD";;
    "${options[2]}" ) selected="SHS";;
    "${options[3]}" ) selected="REM";;
    "${options[4]}" ) selected="SSI";;
    "${options[5]}" ) selected="FOR";;
    "${options[6]}" ) selected="HSS";;
    "${options[7]}" ) selected="HLP";;
    *) continue
    esac
    go $selected
done
}

menu # <--- primary program loop
