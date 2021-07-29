![image](https://user-images.githubusercontent.com/11077042/122314019-04e2d180-cedd-11eb-9c60-7f51a835f059.png)

![image](https://user-images.githubusercontent.com/11077042/122314061-12985700-cedd-11eb-8c9a-106e3e8a39ac.png)


# Pirate-Box
This is the new repository for all code I am contributing to the Pirate Box Contest announced in June of 2021. This is the next step (not the final step!) in Ernest Hancock's Pirate Box project.

It includes the Pirate Box IPFS Search Demo and Batch Video Grabber tools. I have now created a folder structure here on github that mirrors that of the Pirate Box for software I created, most of which lives in the /home/ipfs/bin folder. I also added systemd files, symbolic links and various other files such as documentation and videos. These are not tracked as well, and are found in the Miscellaneous folder. Other application packages and additions were added to the base Raspberry Pi (buster) OS to create the Pirate Box. Here is the text I have for the "About Pirate Box" menu item:


                  pBoxSearch v0.0.2 - Thomas Freedman - 6/17/2021

This prototype Pirate Box was created by Thomas Freedman as a foundation to build a more refined and grandma friendly product. It is a standalone IPFS node customized to demonstrate portable, personal and out of the box functionality including:

--------------------------------------------------
Basic IPFS Node and User Interface

This is provided through the Chromium web browser with the IPFS Companion extension, which is the same User Interface found in IPFS Desktop. Node status, real time graphics of network utilization, ability to view, download, pin and unpin files, inspect IPFS configuration and other useful tools are provided. See  https://github.com/ipfs-shipyard/ipfs-companion or  https://docs.ipfs.io/install/ipfs-desktop/#windows.

----------------------------------------
Pirate Box IPFS Search Tool

This tool implements search functionality based on metadata collected when content is added to an IPFS node. Much more work is required to define the standards for metadata and how it will be collected. 

The search tool uses the metadata to find content by allowing the user to define a filter to locate content of interest based on their specific search criteria.

The IPFS Search Demo tool uses the metadata captured by the Video Grabber tool. A subset of the metadata provided by the youtube-dl program serves as one model (data schema) for audio and video content. 

It's important to note only content captured by the Video Grabber tool is currently searchable. Two IPFS video / audio repositories with well over 12,000 items published in the past 2 years from platforms such as youtube, Vimeo, Brightcove and others are searchable. New content is provided daily and is within the scope of the search tool. Content from over 20 publishers is provided on those 2 IPFS repositories. In addition, the "Liberty Library" content is also searchable (see below).

Audio and video content added to the local Pirate Box IPFS node using the Video Grabber program is also searchable, however that capability is not yet fully developed nor a GUI for it yet designed.

Other types of content providers besides audio and video will have different requirements for their metadata. More work needs to be done to define how metadata is:

                        1) defined
                        2) collected
                        3) published
                        4) represented in search tools

The search tool uses 20 metadata fields out of the 60+ available in the youtube-dl set. Whether a universal standard metadata definition can or will be developed to encompass all types of content has yet to be determined. 

---------------------------------------------
Pirate Box Video Grabber (PBVG)

The PBVG tool was originally developed as a command line program that uses the popular youtube-dl software to download content from a list of over 1000 platforms such as youtube and Vimeo. The full functionality of the program is available as a  "batch" oriented command line tool. However, with this release of the Pirate Box a simple GUI front end is now available to provide an easy to use interface to obtain content from a list of URLs. Content obtained this way is also searchable using the pirate Box Search tool.

Batch mode provides the ability to specify filter criteria such as upload date, duration of play and download quota limits. In addition, content from many different publishers on various platforms can be collected. A scheduler such as cron or systemd timers can automate collection of content from your favorite sources on a regular basis.

The content to be captured by the PBVG is defined in a JSON formated config file that specifies the URLs to download content from, which can be individual files, channels or playlists. Metadata for each item downloaded is also collected. The metadata and the video / audio content files are stored in a SQLite database and published at a static IPnS address for retrieval and use by search engines.

Further refinement of the PBVG is envisioned including a more comprehensive GUI front end to create the JSON config file. The search tool previously described is capable of searching any content added to te Pirate Box using the PBVG.

--------------------
Liberty Library

This release of the Pirate Box includes software infrastructure that supports plug & play content referred to as Liberty Libraries. Portable USB storage devices and USB sticks in very large capacities (currently up to 2 Terabytes) can store huge volumes of information on a  simple USB stick. One example I created was a 512GB drive containing almost 1800 long play format (60 - 90 minutes each) video and audio files saved on IPFS over the last 2 years by Thomas Freedman. This content is available and can be pinned on Pirate Box IPFS nodes or saved on portable Liberty Library devices. Liberty Library content can also be searched with the Pirate Box Search tool described above.


-------------------------------
Hotspot Control 

To provide additional flexibility for "headless" use cases and others requiring additional network options, I have integrated the autohotspot scripts from [RaspberryConnect.com](https://github.com/RaspberryConnect).The integration presents all options in a GUI menu along with a popup help panel to explain each of them. With the correct choice the Pirate Box can power up as an Access Point (hotspot) to facilitate connecting to it from a tablet, laptop or smartphone via WiFi. If the Pirate Box is also connected to the Internet through the wired Ethernet port, then devices connected via the WiFi hotspot can also have Internet.
