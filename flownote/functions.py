#!/usr/bin/env python
#--!-- coding: utf8 --!--

import os, re, json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def appPath(suffix=None):
    p = os.path.realpath(os.path.join(os.path.split(__file__)[0], ".."))
    if suffix:
        p = os.path.join(p, suffix)
    return p

def loadJSON(path):
    with open(appPath(path)) as f:    
        return json.load(f)

def countWords(words):
    r = {}
    for w in words:
        if w in r:
            r[w] += 1
        else:
            r[w] = 1
    return r
    
def countDicts(dicts):
    r = {}
    for d in dicts:
        for w in d:
            if w in r:
                r[w] += d[w]
            else:
                r[w] = d[w]
    return r

UID = 0    
def uniqueID():
    global UID
    UID += 1
    return UID