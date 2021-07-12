Grabber Quickstart
------------------

1) Copy the ytdl-exampleConfig.json file to a name of your chosing in the config folder.
2) Edit the copy to remove the example grupes and add your own.
3) Run the program with:

/home/ipfs/bin/videoGrabber/ytdlVideoGrabber.py -c /home/ipfs/bin/videoGrabber/<your config file> -d <anyNameUwant.sqlite>

The videos / audios at the URLs in the config file will be downloaded to the ytDL dl folder and added to IPFS.
A SQLite database <anyNameUwant.sqlite> will also be created with the information about the downloads.

This can be run from cron scheduler to capture new content regularly.

To publish your newest SQLite database on IPFS you will need to create a static IPnS name and add the hash for that in the ytdlServerDefinitions.py file. Line 213 of ytdlVideoGrabber.py also must be removed or commented out.

Please take note this tool is not intened for "grandma" to use in its' current form, but rather those with a little tech saavy who can read python3 code or the comments in ytdlVideoGrabber.py
