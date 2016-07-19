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
    __mplayer  = None
    __iplayer  = None
    __nowindex = 0
    __queindex = -1

    __thread     = None
    __mutex      = None
    __stop_event = None
    __next_event = None

    __command    = None
    
    def __init__(self,playlist):
        self.__playlist = playlist 
        self.__playmap  = { v["func"]:i for (i,v) in enumerate(playlist)}
        self.__mplayer = movieplayer.MoviePlayer()
        self.__iplayer = imageviewer.ImageViewer()
        self.__nowindex = 0
        self.__stop_event = threading.Event()
        self.__next_event = threading.Event()
        self.__mutex = threading.Semaphore(1)

        self.__command = {
            "play" : self.start,
            "stop" : self.stop,
            "next" : self.playNext,
            "prev" : self.playPrev,
        }
        pass

    def command(self,command):
        if command in self.__command:
            self.__command[command]()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        pass
    
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
        i = self.__getPrevIndex(self.__nowindex)
        self.__queindex = i
        self.__next_event.set()
        self.__mutex.release()
    
    def playNext(self, funcnum = -1):
        self.__mutex.acquire()
        i = self.__playmap[funcnum] if funcnum in self.__playmap else self.__getNextIndex(self.__nowindex)
        self.__queindex = i
        self.__next_event.set()
        self.__mutex.release()
    
    def __play(self):
        while not self.__stop_event.is_set():
            v = self.__playlist[self.__nowindex]
            self.__iplayer.stop()
            self.__mplayer.stop()

            mimetype,subtype = mimetypes.guess_type(v["file"])
            player = self.__iplayer if "image" in mimetype else self.__mplayer

            self.__next_event.clear()
            def endcallback():
                self.__next_event.set()
            
            player.play(v,callback = endcallback)

            while not self.__next_event.wait(1):
                if self.__stop_event.is_set():
                    break
                
            player.stop()

            queindex = self.__queindex
            self.__nowindex = queindex if queindex >= 0 else self.__getNextIndex(self.__nowindex)
            self.__queindex = -1

        self.__iplayer.stop()
        self.__mplayer.stop()
            
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

    def stop(self):
        self.__mutex.acquire()
        try:
            if self.__thread:
                self.__stop_event.set()
                self.__thread.join()
                self.__thread = None
                return True
            else:
                return False
        finally:
            self.__mutex.release()

