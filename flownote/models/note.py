#!/usr/bin/env python
# --!-- coding: utf8 --!--

import re

import flownote.functions as F
from PyQt5.QtCore import *

class Note:
    
    #tagsChanged = pyqtSignal()
    #wordsChanged = pyqtSignal()
    
    def __init__(self, date=None, text="", title="", fromText=""):
        if not fromText:
            # We are creating a new note
            self.date = date
            self.text = text
            self.title = title
        
        if fromText:
            # Creating from a disk file
            self.fromText(fromText)
        
        self.UID = F.uniqueID()
        self._words = None
        self._tags = None
        self._filename = None
        
    def tags(self):
        "Returns all tags within the note."
        if not self._tags:
            self._tags = self.generateTags()
            
        return self._tags
        
    def generateTags(self):
        tags = re.compile('[\w#]+').findall(self.text)
        tags = [t.lower() for t in tags if t[0] == "#"]
        return F.countWords(tags)
        
    def words(self):
        "Returns all words within the note."
        if not self._words:
            self._words = self.generateWords()
            
        return self._words
        
    def wordCount(self):
        return len(re.compile('\w+').findall(self.text))
        
    def generateWords(self):
        "Returns a dict of words with the number of time they appear in the note."
        words = re.compile('[\w#]+').findall(self.text)
        words = [w.lower() for w in words if w[0] != "#"]
        
        return F.countWords(words)
    
    def setDate(self, date):
        self.date = date.toString(Qt.ISODate)
    
    def setText(self, text):
        self.text = text
        t = self.generateTags()
        if t != self._tags:
            self._tags = t
            #self.tagsChanged.emit()
    
    def setTitle(self, title):
        self.title = title
        #FIXME: send signal to update views
           
#==============================================================================
#   LOAD / SAVE
#==============================================================================
    
    def toText(self):
        # Metadata, pandod_title_block style
        t = "% {title}\n% {author}\n% {date}\n\n{content}".format(
            title=self.title,
            author="",
            date=self.date,
            content=self.text)
        return t
    
    def fromText(self, text):
        lines = text.split("\n")
        self.title = lines[0][2:]
        self.date = lines[2][2:]
        self.text = "\n".join(lines[4:])
        