#!/usr/bin/env python
# --!-- coding: utf8 --!--

import re

import flownote.functions as F

class Note():
    
    def __init__(self, date=None, text=""):
        self.date = date
        self.text = text
        self.UID = F.uniqueID()
        
        self._words = None
        self._tags = None
        self._filename = None
        
    def tags(self):
        "Returns all tags within the note."
        if not self._tags:
            self.generateTags()
            
        return self._tags
        
    def generateTags(self):
        tags = re.compile('[\w#]+').findall(self.text)
        tags = [t.lower() for t in tags if t[0] == "#"]
        self._tags = F.countWords(tags)
        
    def words(self):
        "Returns all words within the note."
        if not self._words:
            self.generateWords()
            
        return self._words
        
    def wordCount(self):
        return len(re.compile('\w+').findall(self.text))
        
    def generateWords(self):
        "Returns a dict of words with the number of time they appear in the note."
        words = re.compile('[\w#]+').findall(self.text)
        words = [w.lower() for w in words if w[0] != "#"]
        
        self._words = F.countWords(words)
        