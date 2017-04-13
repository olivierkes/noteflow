#!/usr/bin/env python
# --!-- coding: utf8 --!--

import re

import noteflow.functions as F
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
        t.changed.connect(self.tagsChanged)
        self.tagsChanged.emit()

    def toListLower(self):
        return [t.text.lower() for t in self._tags]

    def find(self, text):
        t = [t for t in self._tags if text.lower() == t.text.lower()]
        if t:
            return t[0]

    def contains(self, tag):
        return tag.lower() in self.toListLower()
            
    def match(self, note):
        for t in self._tags:
            if t.match(note):
                return t
        return False
    
    def removeTag(self, text):
        t = self.find(text)
        if not t:
            return
        self._tags.remove(t)
        self.tagsChanged.emit()

    def __iter__(self):
        return iter(self._tags)

class Tag(QObject):
    
    changed = pyqtSignal()
    
    def __init__(self, text, color=None, background=None, border=None):
        QObject.__init__(self)
        
        self.text = text if text[0] == "#" else "#"+text
        self.color = QColor(color) if color else None
        self.background = QColor(background) if background else None
        self.border = QColor(border) if border else None
        
    def match(self, note):
        return self.text.lower() in note.text.lower()
    
        