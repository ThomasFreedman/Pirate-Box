Grabber Quickstart for Batch Operation
--------------------------------------

NOTE: A newer PDF version of this file can be found in the Documents folder.

1) Copy the ytdl-exampleConfig.json file to a name of your chosing in the config folder.
2) Edit the copy to remove the example grupes and add your own.
3) Run the program with:
 
/home/ipfs/bin/videoGrabber/ytdlVideoGrabber.py -c /home/ipfs/bin/videoGrabber/<your config file> -d example.sqlite

The videos / audios at the URLs in the config file will be downloaded to the ytDL dl folder and added to IPFS. The example.sqlite SQLite database will also be updated with the information about the downloads. You can use the Pirate Box Search tool to find the downloads you're interested in by selecting "PBVG Database" under the File--> Open Search Source menu.

This can be run from the cron scheduler to capture new content regularly.

To publish your newest SQLite database on IPFS you will need to create a static IPnS name and add the hash for that in the ytdlServerDefinitions.py file. 

Please take note this tool is not intened for "grandma" to use in its' current form, but rather those with a little tech saavy who can read python3 code or the comments in ytdlVideoGrabber.py

The tool for grandma is "Pirate Box Video Grabber" currently found under the "Advanced & Experimental Tools" menu. It should be moved to the main Pirate Box menu.
