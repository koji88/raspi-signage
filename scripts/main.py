#!/usr/bin/env python
# -*- coding:utf-8

from __future__ import print_function

import sys
import time
import argparse
import gpiocontroller as GPIOController
import playlist as Playlist
import config as Configure
from twisted.internet import reactor


isQuiet = False

def myprint(f):
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

    isQuiet = args.quiet

    conf = Configure.Configure(args.conf)
    gpiomap= conf.getGPIOMap()
    gpion  = conf.getGPION()
    option = conf.getOption()
    command= conf.getCommand()

    with Playlist.Playlist(conf.getPlaylist()) as playlist:
        playlist.start()
        time.sleep(3)
        playlist.playNext()
        reactor.run()
    

if __name__ == "__main__":
    main()
    
