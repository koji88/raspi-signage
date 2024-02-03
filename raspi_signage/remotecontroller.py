#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import json
import SimpleHTTPServer
import SocketServer
import threading

class JsonCallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    __callback = None
    
    def __init__(self, callback,  *args):
        self.__callback = callback
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        content_len = int(self.headers.get("content-length"))
        requestBody = self.rfile.read(content_len).decode("UTF-8")
        print("JSON=" + requestBody)
        # requestBody = "{"user" : "test", "params" : {"id" : 123, "data" : 5}}"
        jsonData = json.loads(requestBody)

        result = self.__callback(jsonData) if self.__callback else False

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        responseData = json.dumps({"result" : result})
        self.wfile.write(responseData.encode("UTF-8"))

class RemoteController(object):
    __thread     = None
    __mutex      = None
    __stop_event = None
    __port = 8888
    __timeout = 3

    def __init__(self, port = 8888,timeout = 3):
        self.__stop_event = threading.Event()
        self.__mutex = threading.Semaphore(1)
        self.__port = port
        self.__timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        pass

    def __start(self, timeout, callback):
        def handler(*args):
            JsonCallbackHandler(callback, *args)

        server = SocketServer.TCPServer(('', self.__port), handler)
        server.timeout = timeout

        while not self.__stop_event.is_set():
            server.handle_request()

    def start(self, callback):
        self.__mutex.acquire()
        try:
            if self.__thread and self.__thread.is_alive():
                return False
            else:
                self.__stop_event.clear()
                self.__thread = threading.Thread(target = self.__start,args=(self.__timeout,callback))
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
        
        
