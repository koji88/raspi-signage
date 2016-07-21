#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sysfs.gpio import Controller, OUTPUT, INPUT, BOTH
import time

class GPIOController:
    __pullup = False
    __bouncetime = 0.1
    __bouncemap = {}
    
    def __init__(self, gpiopins, pullup = False, bouncetime = 20):
        Controller.available_pins = gpiopins
        self.__pullup = pullup
        self.__bouncetime = bouncetime*0.001

    def allocate(self, gpiopins, pressed_callback = None):
        ison = 1 if not self.__pullup else 0
        def inputChanged(number,state):
            dt = time.time()
            if state == ison and dt > self.__bouncemap[number] + self.__bouncetime:
                self.__bouncemap[number] = dt
                pressed_callback(number)
        
        for pin in gpiopins:
            Controller.alloc_pin(pin, INPUT, inputChanged if pressed_callback else None, BOTH)
            self.__bouncemap[pin] = time.time()
            
    def getState(self,number):
        state = Controller.get_pin_state(number)
        return state if not self.__pullup else not state

    def getBinary(self,gpion):
        n = 0
        for i,v in enumerate(gpion[::-1]):
            if self.getState(v):
                n |= (1<<i)
        return n
    
