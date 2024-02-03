#!/usr/bin/env python
# -*- coding: utf-8 -*-



import pexpect
import threading

class MoviePlayer(object):
    __thread     = None
    __mutex      = None
    __stop_event = None
    __audio_out  = None

    __CMD_PLAYER= '/usr/bin/omxplayer'
    __CMD_PAUSE = 'p'
    __CMD_QUIT  = 'q'
    
    def __init__(self,audio_out):
        self.__stop_event = threading.Event()
        self.__mutex = threading.Semaphore(1)
        self.__audio_out = audio_out
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        pass

    def __play(self, filename, loop, args,callback):
        cmd = "{0} {1} {2} {3} {4} --no-osd".format(self.__CMD_PLAYER,filename
                                                    ,"--loop" if loop else ""
                                                    ,"-o {0}".format(self.__audio_out) if self.__audio_out else ""
                                                    ,args)
        print(cmd)
        p = pexpect.spawn(cmd)

        while not self.__stop_event.is_set():
            i = p.expect([pexpect.EOF, pexpect.TIMEOUT],timeout = 1)
            if i == 0:
                break

        p.send(self.__CMD_QUIT)
        p.terminate(force=True)
        if callback:
            callback()

    def play(self, item,callback = None):
        self.__mutex.acquire()

        filename = item["file"]
        loop     = item["loop"] if "loop" in item else False
        args     = ""

        try:
            if self.__thread and self.__thread.is_alive():
                return False
            else:
                self.__stop_event.clear()
                self.__thread = threading.Thread(target = self.__play,args=(filename,loop,args,callback))
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

    def isplaying(self):
        self.__mutex.acquire()
        try:
            return self.__thread and self.__thread.is_alive()
        finally:
            self.__mutex.release()                
            
