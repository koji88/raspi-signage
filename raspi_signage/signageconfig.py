#!/usr/bin/env python
# -*- coding: utf-8 -*-



import yaml
from collections import OrderedDict

yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))

class Configure:
    __data = None

    def __init__(self, yamlfile):
        self.__data = yaml.load(file(yamlfile))

    def getOption(self):
        return self.__data["option"]

    def getPlaylist(self):
        return self.__data["playlist"]
    
    def getCommand(self):
        return self.__data["command"]

    def getGPIOMap(self):
        d = {v:k for k, v in list(self.__data["gpiomap"].items()) if type(k) == int}
        if "ntri" in self.__data["gpiomap"]:
            d[self.__data["gpiomap"]["ntri"]] = "ntri"
        return d

    def getGPION(self):
        return self.__data["gpiomap"].get("n",[])
    
