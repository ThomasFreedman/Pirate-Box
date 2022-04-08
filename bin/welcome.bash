#!/bin/bash
if [ -f welcome.off ]; then exit; fi

TITLE='Welcome!'
MSG='The welcome screen is now disabled.'
zenity --filename="$HOME/bin/welcome.txt" --text-info --title="$TITLE" --width=520 --height=400
if [ $? -ne 0 ]; then
  zenity --question --text="Stop showing this at startup?" --width=150 --height=100
  if [ $? -eq 0 ]; then
    zenity --title="Disabling Welcome..." --info --text="$MSG" --width=280 --height=100
    touch welcome.off
    exit
  fi
fi



