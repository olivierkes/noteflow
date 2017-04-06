#!/usr/bin/env python
# --!-- coding: utf8 --!--

import re

import flownote.functions as F
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TagCollector(QObject):
    
    tagsChanged = pyqtSignal()    
    
    def __init__(self):
        QObject.__init__(self)
        self._tags = []
        
    def addTag(self, text, color=None, background=None, border=None):
        t = Tag(text, color=color, background=background, border=border)
        self._tags.append(t)
        self.tagsChanged.emit()
        
    def toListLower(self):
        return [t.text.lower() for t in self._tags]
        
    def find(self, text):
        t = [t for t in self._tags if text.lower() == t.text.lower()]
        if t:
            return t[0]
            
    def match(self, note):
        for t in self._tags:
            if t.match(note):
                return t
        return False
            
    def __iter__(self):
        return iter(self._tags)

class Tag(QObject):
    
    def __init__(self, text, color=None, background=None, border=None):
        QObject.__init__(self)
        
        self.text = text if text[0] == "#" else "#"+text
        self.color = QColor(color) if color else None
        self.background = QColor(background) if background else None
        self.border = QColor(border) if border else None
        
    def match(self, note):
        return self.text.lower() in note.text.lower()
    
        