#!/usr/bin/env python
# -*- coding:utf-8

from __future__ import print_function

import sys
import time
import argparse
import gpiocontroller as GPIOController
import playlist as Playlist
import signageconfig as Configure
from twisted.internet import reactor


isQuiet = False

def myprint(f):
    global isQuiet
    if not isQuiet:
        print(f)

def main():
    p = argparse.ArgumentParser(description='Raspberry pi Digital Signage')
    p.add_argument('-c','--conf',help="configuration yaml filename")
    p.add_argument('--quiet',action='store_true',help="quiet mode")
    args = p.parse_args()

    if not args.conf:
        print("configuration file is not supplied")
        return

    global isQuiet
    isQuiet = args.quiet

    conf = Configure.Configure(args.conf)
    gpiomap= conf.getGPIOMap()
    gpion  = conf.getGPION()
    option = conf.getOption()
    command= conf.getCommand()

    with Playlist.Playlist(conf.getPlaylist(),option) as playlist:
        playlist.start()
        
        gpio = GPIOController.GPIOController(gpiomap.keys() + gpion, pullup = option["pullup"])

        def sw_pressed(gpiopin):
            num = gpiomap[gpiopin]
            if num == "ntri":
                num = gpio.getBinary(gpion)
            
            myprint("gpio {0} is pressed: funcnum {1}".format(gpiopin,num))
            if option["exit"] == num:
                reactor.stop()
                return

            if num in command:
                playlist.command(command[num])
                return

            playlist.play(num)
        
        gpio.allocate(gpiomap.keys(),sw_pressed)
        gpio.allocate(gpion)
    
        reactor.run()

    

if __name__ == "__main__":
    main()
    
