#!/bin/bash

INSTALLPATH=/usr/src/raspi-signage
MOUNTPOINT=/mnt/usbdisk
USBMEMORY=/dev/disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1
CONFIGFILE=raspi-signage.yml
UPDATEFILE=raspi-signage-update.txt

if [ ! -d $MOUNTPOINT ]; then
    mkdir $MOUNTPOINT
fi

if [ -e $USBMEMORY ]; then
    echo "Find target USB Memory, mount it."
    mount -t vfat $USBMEMORY $MOUNTPOINT
else
    echo "Cannot find target USB Memory, please insert it."
    exit 1
fi

if [ -e "$MOUNTPOINT/$UPDATEFILE" ]; then
    echo "Update raspi-signage scripts"
    cd $INSTALLPATH
    git pull
    rm -rf /usr/local/lib/python2.7/dist-packages/raspi_signage-*
    python setup.py install
    rm "$MOUNTPOINT/$UPDATEFILE"
    shutdown -r now
    exit 0
fi

echo "Launch raspi-signage"
setterm -blank 0 -cursor off
clear
raspi-signage -c $MOUNTPOINT/$CONFIGFILE >/dev/null 2>&1

exit 0
