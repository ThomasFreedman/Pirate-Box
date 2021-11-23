![image](https://github.com/ThomasFreedman/Pirate-Box/blob/main/pboxMenus0.0.5.jpg?raw=true)

![image](https://user-images.githubusercontent.com/11077042/122314061-12985700-cedd-11eb-8c9a-106e3e8a39ac.png)


# Pirate-Box
This is the new repository for all code I am producing for the Pirate Box. This project was started in February 2021 when Ernest Hancock gave his positive endorsement on Telegram's "Pirate Box Project" group to create a "Pirate Box" based on the popular Raspberry Pi computer that had an IPFS node and IPFS Companion installed as a basic user interface. This code repository is my attempt to meet Ernest's continuously changing requirements for a Pirate Box, despite delivering on the original idea in April.

The Pirate Box is now far more than a basic IPFS node and IPFS Companion browser extention I originally proposed. Here is a summary of its' current features: 

                  pBoxSearch v0.0.5 - Thomas Freedman - 11/19/2021

This prototype Pirate Box was created by Thomas Freedman as a foundation to build a more refined and grandpa friendly product. This release of the Pirate Box uses the recently released 64 bit version of Raspberry Pi OS. It is a standalone IPFS node customized to demonstrate portable, personal and out of the box functionality including:

--------------------------------------------------
***Basic IPFS Node and User Interface***

This is provided through the Chromium web browser with the IPFS Companion extension, which is the same User Interface found in IPFS Desktop. Node status, real time graphics of network utilization, ability to view, download, pin and unpin files, inspect IPFS configuration and other useful tools are provided. See  https://github.com/ipfs-shipyard/ipfs-companion or  https://docs.ipfs.io/install/ipfs-desktop/#windows.  

----------------------------------------
***Pirate Box IPFS Search Tool***

This tool implements search functionality based on metadata collected when content is added to an IPFS node. Much more work is required to define the standards for metadata and how it will be collected. 

The search tool uses the metadata to find content by allowing the user to define a filter to locate content of interest based on their specific search criteria.

The IPFS Search Demo tool uses the metadata captured by the Video Grabber tool. A subset of the metadata provided by the youtube-dl program serves as one model (data schema) for audio and video content. 

It's important to note only content captured by the Video Grabber tool is currently searchable. Two IPFS video / audio repositories with well over 12,000 items published in the past 2 years from platforms such as youtube, Vimeo, Brightcove and others are searchable. New content is provided daily and is within the scope of the search tool. Content from over 20 publishers is provided on those 2 IPFS repositories. In addition, the "Liberty Library" content is also searchable (see below).

Providers of content types besides audio and video will have different requirements for their metadata. More work needs to be done to define how metadata is:

                        1) defined
                        2) collected
                        3) published
                        4) represented in search tools

The search tool uses 20 metadata fields out of the 60+ available in the youtube-dl set. Whether a universal standard metadata definition can or will be developed to encompass all types of content has yet to be determined. 

----------------------------------------------
***Pirate Box Video Grabber (PBVG)***

The PBVG tool was originally developed as a command line program that uses the popular youtube-dl software to download content from a list of over 1000 platforms such as youtube and Vimeo. The full functionality of the program is available as a  "batch" oriented command line tool. However, with this release of the Pirate Box a simple GUI front end is now available to provide an easy to use interface to obtain content from a list of URLs. Content obtained this way is also searchable using the Pirate Box Search tool.

Batch mode operation provides the ability to be selective of the content gathers using filter criteria such as upload date, duration of play and download quota limits. In addition, content from many different publishers on various platforms can be collected frequently. A scheduler such as cron can automate collection of content from your favorite sources on a regular basis.

The content to be captured by the PBVG is defined in a JSON formated config file that specifies the URLs to download content from, which can be individual files, channels or playlists. Metadata for each item downloaded is also collected. The metadata and the video / audio content files are stored in a SQLite database and published at a static IPnS address for retrieval and use by search engines.

Further refinement of the PBVG is envisioned including a more comprehensive GUI front end to create the JSON config file. The search tool previously described is capable of searching any content added to te Pirate Box using the PBVG.

--------------------
***Liberty Library***

This release of the Pirate Box includes software infrastructure that supports plug & play content referred to as Liberty Libraries. Portable USB storage devices and USB sticks in very large capacities (currently up to 2 Terabytes) can store huge volumes of information on a  simple USB stick. One example I created was a 512GB drive containing almost 1800 1000 long play format (60 - 90 minutes each) video and audio files saved on IPFS over the last 2 years by Thomas Freedman. This content is available and can be pinned on Pirate Box IPFS nodes or saved on portable Liberty Library devices. Liberty Library content can also be searched with the Pirate Box Search tool described above.

----------------------
***Hotspot Control***

The autohotspot software from RaspberryConnect.com provide many options to control the networking, including WiFi hotspots for the Pirate Box. It is now possible to start the Pirate Box "headless" (no screen or keyboard) and operate it as a battery powered, WiFi hotspot.

----------------------------------------
***Upgrade to External Storage***

SD Cards are wonderful for their small size, but they aren't the best for long term, reliable use. It can be a complicated process to setup external storage, but it is now possible to migrate or upgrade the IPFS storage on your Pirate Box to an external USB device such as a portable hardrive or Solid State Drive (SSD).

---------------------------------------
***Offline IPFS Documentation***

This release also includes a complete copy of the IPFS documentation from the docs.ipfs.io website, updated slightly for use on the Pirate Box while offline. Tutorials are included for migrating websites to IPFS. 

------------------------
***Nginx Webserver***

To serve the documentation and provide support for other homegrown web applications, the Pirate Box now includes it's very own webserver. 

---------------------------------
***Support for Moonbeam***

Moonbeam, a self publisher solution from agoristhosting.com is a browser based application that provides a way to capture and publish content to IPFS. When Moonbeam becomes available, it can be used on the Pirate Box. A simple to use tool to create, list and remove keys for use with Moonbeam or IPNS is now included.

-------------------------------------
***Support for Mesh Networks***

Support for 3 different mesh netwoking protocols and associated documentation is now included in this release. The 3 mesh protocols are XMPP / Jabber (the prosody client), Reticulum and yggdrasil. None of these are configured. The documentation is available offline directly from the Pirate Box *Advanced and Experimental* submenu.

