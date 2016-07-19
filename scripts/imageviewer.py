#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import time
import threading

class ImageViewer(object):
    __thread     = None
    __mutex      = None
    __stop_event = None

    __CMD_VIEWER= "/usr/bin/fbi"
    __CNF_FB = "/dev/fb0"
    __CNF_ARG = "-noverbose -a -T 2"
    
    def __init__(self):
        self.__stop_event = threading.Event()
        self.__mutex = threading.Semaphore(1)
        self.__clear()
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        pass

    def __play(self,filename,timeout,callback):
        cmd = "{0} -d {1} {2} {3}".format(
            self.__CMD_VIEWER,
            self.__CNF_FB,
            self.__CNF_ARG,
            filename)
        print(cmd)
        os.system(cmd)

        if timeout > 0:
            for i in range(timeout):
                if self.__stop_event.is_set():
                    break
                time.sleep(1)
        else:
            while not self.__stop_event.is_set():
                time.sleep(1)

        os.system("killall -9 {0}".format(self.__CMD_VIEWER))
        self.__clear()
        if callback:
            callback()

    def play(self, item,callback=None):
        self.__mutex.acquire()

        filename = item["file"]
        timeout  = item["timeout"]
        print(filename)
        
        try:
            if self.__thread and self.__thread.is_alive():
                return False
            else:
                self.__stop_event.clear()
                self.__thread = threading.Thread(target = self.__play,args=(filename,timeout,callback))
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

    def __clear(self):
        os.system("dd if=/dev/zero of={0}".format(self.__CNF_FB))

    def isplaying(self):
        self.__mutex.acquire()
        try:
            return self.__thread and self.__thread.is_alive()
        finally:
            self.__mutex.release()                
