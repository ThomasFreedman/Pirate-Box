Available options

 1 = Autohotspot with Internet for connected devices
 2 = Autohotspot with no Internet for connected devices
 3 = Permanent Hotspot with Internet for connected devices
 4 = Uninstall Autohotspot or Permanent Hotspot
 5 = Scan for a new WiFi network (SSID) or change existing ones
 6 = Force to a Hotspot or Force to Network if SSID in Range
 7 = Change the Hotspots SSID and Password
 8 = Help for each of these options

Explanation of each:

1: Automatic hotspot with Internet for connected devices 
-------------------------------------------------------------------------------
After a reboot this option causes the Raspberry Pi to connect to a router that has previously been connected to and is listed in /etc/wpa_supplicant/ wpa_supplicant.conf. If none of the SSIDs in that file are in range then the Pi will generate a WiFi hotspot. The default SSID will be PirateBoxNNNN and password of @RRRsp0t (Ns are a list of psuedorandom numbers). Use option 7 to change the password and/or the SSID if required.

With this option if an ethernet cable is connected to the Pi with access to the internet then it will allow devices connected to the hotspot access to the internet or local network.

Once a connection to the hotspot has been made you can access the Raspberry Pi via ssh & VNC (ssh: ipfs@192.168.50.2 or vnc: 192.168.50.2::5900. Use your Pi's ipfs account password you set when you setup your Pirate Box).

2: Hotspot for Pirate Box only, no Internet for devices
--------------------------------------------------------------------------
This is similar to option 1 but connected devices have no internet connection. Use this option to only provide access to the Pirate Box from a Laptop, tablet or phone. The hotspot SSID and password are randomly generated as for option 1 though it is generated upon each option selection.

3: Permanent Hotspot with Internet for devices
------------------------------------------------------------------
This is for a permanent WiFi hotspot with internet access for WiFi devices. Network or internet access is available only through the ethernet cable.

Additional work is required to use a second WiFi device to connect to the internet rather than a wired ethernet conection. This will be a future option.

4: Use normal Raspberry Pi wired & wireless networking
------------------------------------------------------------------------------
This will disable the setup of any of the three setups and return the Raspberry Pi to default Wifi settings. Hostapd & dnsmasq will not be uninstalled just disabled.

5: Add/Change WiFi SSID to access the Internet
------------------------------------------------------------------
Use this option to scan for and select a WiFi network to access the Internet. You must use this option instead of the desktop wifi icon in the upper right corner (shown as red crosses) because that is disabled. After rebooting (or using option 6 below) the Pi will connect to this WiFi. You can also manually add the details to /etc/wpa_supplicant/wpa_supplicant.conf if you know them.

This option only works for WiFi networks where only a password is required. If a username is also required this will not work but may in a future update.

6: Force to a Hotspot or Force to Network if SSID in Range
---------------------------------------------------------------------------------
Use this if you are at home and connected to your home network but would like to access the Pirate Box using it's hotspot. This option will force the Pi to hotspot mode and will ignore your home network until the next reboot. If you use this option again while in hotspot mode it will attempt to connect to a known network. This will go back to the hotspot if no valid WiFi network is found or there is a connection issue.
 
7: Change the Hotspots SSID and Password
--------------------------------------------------------------
By default the hotspot SSID and password are set randomly. Use this option to change either or both SSID and Password. You will be prompted to change both but if you make no entry and press enter the existing setting will be kept. NOTE: The password must be at least 8 characters.

8: Help for each of these options -- This ReadMe file
 
NOTES
----------
IMPORTANT: After using the Hotspot Control tool to change the Pirate Box networking setup, you will not be able to select a WiFi connection from the top of the desktop. You must select your Wifi connection from the Hotspot Control menu, option 5. To restore normal desktop WiFi selection to Pirate Box you must disable the hotspot with option 4. Often rebooting helps if you have other network difficulties. 

IPtables / NFtables:
This setup uses iptables for routing the Hotspots to the internet, options 1 and 3. From late releases of Raspberry Pi OS 10 (Buster), IPtables are have been replaced by NFtables. By default NFtables will handle IPtable rules. If you know you are using NFtables for a Firewall or other routing rules then don't use the internet routed hotspots and only use option 2, Autohotspot without internet. Otherwise there will be a conflict with your routing tables.

Support for NFtables will be implemented in the future. Early releases of Raspberry Pi OS (Buster), Raspbian 9 (Stretch) and Jessie (8) use IPtables.

/etc/network/interfaces file:
Many older hotspot and network setup guides online add entries to the /etc/network/interfaces file. This file is depreciated in Raspbian and any entry in this file is not compatible with the Pirate Box Autohotspot. When Autohotspot was installed these entries were backuped and removed. They will be restored if uninstall option 4 is used.

RaspberryConnect.com
