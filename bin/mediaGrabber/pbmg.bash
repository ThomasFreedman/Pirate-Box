#!/bin/bash

BASE=/home/ipfs/bin/mediaGrabber
ADD_URLS=$BASE/addUrls2Template.py
GRABBER=$BASE/ytdlMediaGrabber.py
SQLDB=$BASE/catalog.sqlite

intro() {
  cat <<'EOI'
This tool will ask you for a list of one or more URLs to grab
media content from and use that input to run the Pirate Box
Media Grabber tool. URLs that point to playlists or media files
work best.

The tool will download the content and metadata for it and add
it to IPFS and record that in a SQLite database for use by the
IPFS Search Tool to make it easy to find and filter.
EOI
}

makeBatch() {
  CFG=$($ADD_URLS "$BASE" "$URLS")  # Returns the config file with URLs added
  cat << EOF > /tmp/pbmg.bash
#!/bin/bash
$GRABBER -c $CFG -d $SQLDB
echo "Process complete. Press any key to close this window."
read
EOF
  chmod 755 /tmp/pbmg.bash
}

# Inform user
zenity --info --text="$(intro)" --width=475 --height=100

TITLE='URL List Entry'
MSG='Please enter your comma separated list of URLs'
URLS=$(zenity --entry --title="$TITLE" --text="$MSG" --width=400)

if [ $? -eq 0 ]; then
  # Make sure we're still online with Internet
  $(ping -c 1 1.1.1.1 > /dev/null 2>&1)
  if [ $? -ne 0 ]; then
    zenity --error --text="You're not online!" --width=250
    exit 1
  fi
  # Make sure the local IPFS node is running
  AOK=$(netstat -ln | grep :8080)
  if [ "$AOK" == "" ]; then
    zenity --error --text="IPFS is offline!" --width=250 --height=100
  else
    makeBatch
    TITLE="Pirate Stick Video Grabber"
    lxterminal --geometry=80x20 -t "$TITLE" -e /tmp/pbmg.bash
  fi
else
  MSG="Problem with your list of URLs!\nThe first 4 letters must be 'http'"
  zenity --error --text="$MSG" --width=250 --height=100
fi

