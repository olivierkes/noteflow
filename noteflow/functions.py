#!/usr/bin/env python
#--!-- coding: utf8 --!--

import os, re, json, string

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
    
def settings(key=None, default=None, type=None):
    #~/.config/noteflow/noteflow.conf on my systems
    s = QSettings(qApp.organizationName(), qApp.applicationName())
    if key is None:
        return s
    else:
        if type:
            return type(s.value(key, default))
        else:
            return s.value(key, default)
    
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

def findRowByUserData(table, data):
    "Search in a table userData"
    matches = table.model().match(table.model().index(0,0), Qt.UserRole, data,
                                  flags = Qt.MatchExactly)
    if matches:
        return table.item(matches[0].row(), matches[0].column())
    
def findNoteByUID(notebooks, UID):
    for nb in notebooks:
        for n in nb.notes:
            if n.UID == UID:
                return n
    return None
    
def slugify(name):
    """
    A basic slug function, that escapes all spaces to "_" and all non letters/digits to "-".
    @param name: name to slugify (str)
    @return: str
    """
    valid = string.ascii_letters + string.digits
    newName = ""
    for c in name:
        if c in valid:
            newName += c
        elif c in string.whitespace:
            newName += "_"
        else:
            newName += "-"
    return newName

def loadTextFile(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()
    
def strToDate(date):
    return QDate(*[int(i) for i in date.split("-")])

def stats(text):
    w = len(re.findall(r"\b[\w'-]+\b", text))
    text = text.replace("\n", "")
    c = len(text)
    c2 = len([c for c in text if c.strip()])
    
    return w, c, c2