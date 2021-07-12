#!/usr/bin/env python3
import subprocess as sp
import pyudev
import time
import os


# This code is run on boot by systemd to detect when a  Liberty Library USB
# storage device (USB stck, SSD etc) is inserted or removed from the Pirate
# Box. It spawns a new process to handle the actual event.


def log_event(action, device):
    time.sleep(2) # <--- Crucial to give automounter  time to mount partition
    devName = device.get('DEVNAME')
    devLabel = device.get('ID_FS_LABEL')
    if devLabel == "LIBERTY_LIBRARY":
        sp.Popen(["/home/ipfs/bin/libertyLibrary/usbEvent.py",
                  action, devName, devLabel],
                 stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block', device_type="partition")
observer = pyudev.MonitorObserver(monitor, log_event)
observer.daemon = True
observer.start()

while True:
    time.sleep(2)
