#!/usr/bin/python3

#
# Defines constants for ytdlVideoGrabber.py, a program to scrape videos.
#
EMAIL_SERVR     = ["yourSMTPserverAddress", 'portNumber'] # NOTE: Don't quote portNum!
EMAIL_LOGIN     = ["smtpAccount", "smtpPassword"]
EMAIL_LIST      = "comma separted list of recipients"
EMAIL_URLS      = EMAIL_LIST
STATIC_DB_HASH  = "" # Your SQLite database ipNs address (Optional)
EMAIL_SUB1      = 'email subject line'
EMAIL_SUB2      = 'email subject for (separate) URL email'
EMAIL_FROM      = "the address you want for 'From' line of email"
SEND_EMAIL      = False  # Send results to email recipients or not
SEPARATOR       = "~^~"  # Separates elements of the downloaded file pathname
EXT_LIST        = ("webm", "mp3", "m4a", "mp4", "mkv", "m4v") # File extensions


