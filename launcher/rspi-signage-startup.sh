#!/bin/bash

INSTALLPATH=/usr/src/rspi-signage
MOUNTPOINT=/mnt/usbdisk
USBMEMORY=/dev/disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1
CONFIGFILE=rspi-signage.yml
UPDATEFILE=rspi-signage-update.txt

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
    echo "Update rspi-signage scripts"
    cd $INSTALLPATH
    git pull
    python setup.py install
    exit 0
fi

echo "Launch rspi-signage"
rspi-signage -c $MOUNTPOINT/$CONFIGFILE

exit 0
