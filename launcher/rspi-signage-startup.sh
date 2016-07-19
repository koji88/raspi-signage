#!/bin/bash

MOUNTPOINT=/mnt/usbdisk
USBMEMORY=/dev/disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1
CONFIGFILE=config.yml

if [ ! -d $MOUNTPOINT ]; then
    mkdir $MOUNTPOINT
fi

if [ -e $USBMEMORY ]; then
    echo "Find target USB Memory, mount it."
    mount -t vfat $USBMEMORY $MOUNTPOINT
    echo "Launch rspi-signage"
    rspi-signage -c $MOUNTPOINT/$CONFIGFILE
    echo "Unmount target USB Memory."
    umount $MOUNTPOINT
else
    echo "Cannot find target USB Memory, please insert it."
fi

