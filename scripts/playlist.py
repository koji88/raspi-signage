#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import mimetypes
import movieplayer
import imageviewer
import threading

class Playlist(object):
    __playlist = None
    __playmap  = None
    __option   = None
    __mplayer  = None
    __iplayer  = None
    __nextindex = 0
    __queindex = -1

    __thread     = None
    __mutex      = None
    __stop_event = None
    __next_event = None

    __command    = None
    
    def __init__(self,playlist, option):
        self.__playlist = playlist 
        self.__playmap  = { v["func"]:i for (i,v) in enumerate(playlist)}
        self.__option   = option
        self.__mplayer = movieplayer.MoviePlayer()
        self.__iplayer = imageviewer.ImageViewer(option["clearimage"])
        self.__nextindex = 0
        self.__stop_event = threading.Event()
        self.__next_event = threading.Event()
        self.__mutex = threading.Semaphore(1)

        self.__command = {
            "play" : self.play,
            "stop" : self.stop,
            "next" : self.playNext,
            "prev" : self.playPrev,
        }
        pass

    def command(self,command):
        if command in self.__command:
            print(command)
            self.__command[command]()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop(showidleimage = False)
        self.__mplayer.stop()
        self.__iplayer.stop()
        pass

    def __getOption(self,option):
        return option in self.__option and self.__option[option]
    
    def __getNextIndex(self,index):
        index += 1
        if index >= len(self.__playlist):
            index = 0
        return index

    def __getPrevIndex(self,index):
        index -= 1
        if index < 0:
            index = len(self.__playlist) - 1
        return index
    
    def playPrev(self):
        self.__mutex.acquire()
        i = self.__getPrevIndex(self.__nextindex)
        self.__queindex = i
        self.__next_event.set()
        self.__mutex.release()
        self.start()
    
    def playNext(self):
        self.__mutex.acquire()
        i = self.__getNextIndex(self.__nextindex)
        self.__queindex = i
        self.__next_event.set()
        self.__mutex.release()
        self.start()

    def play(self, funcnum = -1):
        self.__mutex.acquire()
        i = self.__playmap[funcnum] if funcnum in self.__playmap else self.__nextindex
        self.__queindex = i
        self.__next_event.set()
        self.__mutex.release()

        self.start()
        
    def __play(self):
        autostart = self.__getOption("autostart")
        idleimage = self.__option["idleimage"] if "idleimage" in self.__option else None
        self.__mplayer.stop()
        self.__iplayer.stop()
        
        while not self.__stop_event.is_set():

            if not autostart and self.__queindex < 0:
                self.__next_event.clear()
                if not self.__getOption("autonext"):
                    if idleimage:
                        self.__iplayer.play({"file":idleimage,"timeout":-1})
                    
                    while not self.__next_event.wait(1):
                        if self.__stop_event.is_set():
                            return

                    if idleimage:
                        self.__iplayer.stop()
                        
            autostart = False
            
            index = self.__nextindex           
            queindex = self.__queindex
            index = queindex if queindex >= 0 else index
            self.__queindex = -1                
            self.__nextindex = index
            print("quieindex: {0}".format(queindex))
            print("playindex: {0}".format(index))
            v = self.__playlist[index]

            mimetype,subtype = mimetypes.guess_type(v["file"])
            player = self.__iplayer if "image" in mimetype else self.__mplayer

            def endcallback():
                self.__next_event.set()
            
            self.__next_event.clear()
            player.play(v,callback = endcallback)

            while not self.__next_event.wait(1):
                if self.__stop_event.is_set():
                    break
                
            player.stop()
            
            if self.__getOption("autonext"):
                self.__nextindex = self.__getNextIndex(index)            

            
    def start(self):
        self.__mutex.acquire()

        try:
            if self.__thread and self.__thread.is_alive():
                return False
            else:
                self.__stop_event.clear()
                self.__thread = threading.Thread(target = self.__play)
                self.__thread.start()
                return True
        finally:
            self.__mutex.release()

    def stop(self, showidleimage = True):
        self.__mutex.acquire()
        try:
            if self.__thread:
                self.__stop_event.set()
                self.__thread.join()
                self.__thread = None
                if showidleimage:
                    idleimage = self.__option["idleimage"] if "idleimage" in self.__option else None
                    if idleimage:
                        self.__iplayer.play({"file":idleimage,"timeout":-1})
                return True
            else:
                return False
        finally:
            self.__mutex.release()

