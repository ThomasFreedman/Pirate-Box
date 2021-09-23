#!/bin/bash
#
# A simple tool to create, list & remove IPfS keys for use with IPnS

# Make sure IPFS has been setup & is running
if [ -f /home/ipfs/.ipfs/config ]; then
  sudo systemctl is-active --quiet ipfs
  if [ $? -ne 0 ]; then
          MSG="IPFS is not running!\n"
          zenity --error --text="$MSG" --width=150
          exit -1
  fi
else
  MSG1="You have not setup your IPFS node!\n"
  MSG2="Please run the IPFS Setup Wizard."
  zenity --error --text="$MSG1$MSG2" --width=300
  exit -1
fi

TITLE="Create a New Key"
MSG="Enter new key name, or Cancel to list existing keys"
while NAM=$(zenity --entry --title="$TITLE" --text="$MSG")
do
  if [ $? -ne 0 ] || [ "$NAM" == "" ]; then
    break;
  else
    NEW=$(ipfs key gen $NAM)
    TITLE="The key for $NAM is:"
    zenity --info --text="$NEW" --title="$TITLE" --width=300
  fi
done

title="Existing Moonbeam - IPFS Keys"
prompt="Pick a key name and click OK to remove, or Cancel to exit:"
while options=($(ipfs key list))
do
  opt=$(zenity --list --title="$title" --width 460 --height 350 \
               --text="$prompt" --column="Existing Key Names:" \
               "${options[@]}")

  if [ "$opt" != "" ]; then
    $(ipfs key rm $opt > /dev/null)
  else
    break
  fi
done


