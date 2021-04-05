![pbsScreenShot](https://user-images.githubusercontent.com/11077042/113526398-9057f200-957f-11eb-9df6-db931096d147.png)

# Pirate-Box
This is the new repository for all code I am contributing to Ernest Hancock's Pirate Box project.

It includes the Pirate Box IPFS Search Demo and Batch Video Grabber tools. Here is the text I have for the "About" menu item of the search tool:

                             About this Pirate Box

This prototype Pirate Box was created by Thomas Freedman as a foundational platform to build a more refined and grandma friendly product. It is a standalone IPFS node customized to demonstrate portable, personal and out of the box functionality including:

                      Basic IPFS Node and User Interface

This is provided through the Chromium web browser with the IPFS Companion extension, which is the same User Interface found in IPFS Desktop. Node status, real time graphics of network utilization, ability to view, download, pin and unpin files, inspect IPFS configuration and other useful tools are provided. See https://github.com/ipfs-shipyard/ipfs-companion or https://docs.ipfs.io/install/ipfs-desktop/#windows. Note that future versions of Pirate Box will be based on the IPFS Desktop version for better integration with the Raspberry Pi menu system.

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

                                 Video Grabber

The Video (and audio) Grabber tool is a fully functional command line program that uses the popular youtube-dl software to download content from a list of over 1000 platforms such as youtube and Vimeo. It is "batch" oriented, so content from many publishers on many platforms can be collected frequently. A cron job can automate collection of content from your favorite sources on a regular basis.

The content to be captured by the Video Grabber is defined in a JSON formated config file that specifies the URLs to download content from, which can be individual files, channels or playlists. Metadata for each item downloaded is also collected from youtube-dl. The metadata and the video / audo content files are stored in a SQLite database and published at a static IPnS address for retrieval and use by search engines.

Further refinement of the search tool is envisioned including a GUI front end to create the JSON config file. The search tool described above is capable of searching any content added to te Pirate Box using the Video Grabber command line tool.

                                Liberty Library

The Pirate Box prototype includes a 1TB SSD drive / SD card containing hundreds of long play format video and audio content (60 - 90 minutes each) saved on IPFS over the last 2 years by Thomas Freedman. This content is available and pinned on the Pirate Box IPFS node and searchable using the Pirate Box IPFS Search too described above.  

It is reletively easy to use an external IPFS repository filled with content if the external content has the same structure as the .ipfs folder. However that cannot be accessed concurrently with the local IPFS node's content. To make a plug & play "Liberty Library" to add to an existing IPFS node's content would require either 1) merging the 2 repositories into one, or 2) running a second IPFS server instance on the same node using different port numbers.

The Liberty Library included in this release of the Pirate Box used the method of step 1. If the external storage is not plugged in the local IPFS node will fallback to a small repository included on the SD card. Alternatively if the SD card is large enough no external storage device is required.

Currently IPFS does not provide a way to split the storage of a repository into separate segments which would make adding external content like a Liberty Library much easier.


--------------------------------------------------------------------------------------------------
This code is free to use under the terms of the [BipCot NoGov license](https://bipcot.org/). 

BipCot NoGov Software License www.bipcot.org, version 1.2 / No warranty of usability of "Pirate Box" software.

This original computer code and resulting program was made by license holder Thomas Freedman, 2021. All rights to make fun of you reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions and adaptations of source code or program must retain the entirety of this license, including retaining attribution of the license holder of the software.

2. Redistributions in binary form must reproduce the entirety of this license.

3. Neither the name of the license holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission. Furthermore, no attempt will be made to impersonate the person or entity whose software is being used or modified. 

4. Governments, and agents and subcontractors of same, are not permitted to use this software or derivations of this software.

5. If governments, agents and subcontractors of same use this software, or derivations of this software, all agencies and persons directly and knowingly involved may be shamed in public, by name, on the Internet, on radio, and in any media now extant or invented in the future, throughout the known universe and elsewhere, in perpetuity. Governments, agents and subcontractors of same that use this software, or derivations of this software, agree to endure this shaming, without comment or action.

6. Any person or entity that violates any part of this agreement will also be shamed as above, and agrees to endure this shaming, without comment or action.

7. The BipCot NoGov Software License adopts the first 3 clauses of the 3-Clause BSD license (Berkeley Software Distribution license) and adopts the BSD "as is" text at the end. The 3-Clause BSD license is in the Public Domain. However, there is no partnership or endorsement created or implied between the creators or users of The BipCot NoGov Software License and the creators or users of the BSD license, or vise versa.

8. This version allows for "LIBERTARIAN INDULGENCES." i.e. low-level government workers like mailmen and peaceful future Internet freedom hero contractors can use the thing that is licensed. 
But cops, goons, politicians, alphabet soup agency workers, etc, and anyone who carries a gun or orders the use of guns for any government agency is still forbidden. 

9. This license only covers use of the software or media itself. The license holder retains any royalties or publishing rights on usage of the software or media, where applicable. 

THIS SOFTWARE IS PROVIDED BY THE LICENSE HOLDER AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE LICENSE HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
