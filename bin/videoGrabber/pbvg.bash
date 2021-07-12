#!/bin/bash

BASE=/home/ipfs/bin/videoGrabber
ADD_URLS=$BASE/addUrls2Template.py
GRABBER=$BASE/ytdlVideoGrabber.py
SQLDB=$BASE/pbvg.sqlite

intro() {
  cat <<'EOI'
This tool will ask you for a list of one or more URLs to grab
media content from and use that input to run the Pirate Box
Video Grabber (PBVG) tool, which will scrape the URL(s), add
the media to IPFS and add the metadata for it to a SQLite
database used by the Pirate Box Search Tool.
EOI
}

# Inform user
zenity --info --text="$(intro)" --width=475 --height=100

TITLE='URL List Entry'
MSG='Please enter your comma separated list of URLs'
URLS=`zenity --entry --title="$TITLE" --text="$MSG" --width=400 --height=50`

pushd $BASE > /dev/null 2>&1
CFG=$($ADD_URLS "$BASE" "$URLS")  # Returns the config file with URLs added

if [ $? -eq 0 ]; then
  # Make sure we're still online with Internet
  $(ping -c 1 1.1.1.1 > /dev/null 2>&1)
  if [ $? -ne 0 ]; then
    zenity --error --text="You're not online!" --width=250 --height=100
    exit 1
  fi
  # Make sure the local IPFS node is running
  AOK=$(netstat -ln | grep :8080)
  if [ "$AOK" == "" ]; then
    zenity --error --text="IPFS is offline!" --width=250 --height=100
  else
    # All systems go, run the grabber. Too bad lxterminal can't be positioned!
    #
    # Too bad xterm & lxterm doesn't allow copy to clipboard!
    # lxterm -geometry 80x20+150+100 -fa 'Monospace' -fs 12 -title "$TITLE"  -e "$CMD"
    CMD="$GRABBER -c $CFG -d $SQLDB; bash"
    TITLE="Pirate Box Video Grabber"
    echo "lxterminal -geometry=80x20 -t $TITLE -e $CMD"
    lxterminal --geometry=80x20 -t "$TITLE"  -e "$CMD"
    #$($GRABBER -c $CFG -d $SQLDB >> pbvg.log 2>&1)
  fi
else
  MSG="Problem with your list of URLs!\nthey must all start with 'http'"
  zenity --error --text="$MSG" --width=250 --height=100
fi
popd > /dev/null 2>&1



