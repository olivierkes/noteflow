#!/usr/bin/env python
# --!-- coding: utf8 --!--

import json
import flownote.functions as F

class Notebook():
    """A collection of notes.

    On the computer, a notebook is a folder containing text files.
    """
    
    def __init__(self, name):
        self.name = name
        self.notes = []
        
#        self._words = None
#        self._tags = None
        
#    def tags(self):
#        "Returns all tags within the Journal."
#        if not self._tags:
#            self.generateTags()
#            
#        return self._tags
#        
#    def generateTags(self):
#        "Generate list of tags."
#        self._tags = F.countDicts([n.tags() for n in self.notes])
#        
#    def words(self):
#        "Returns all words within the note."
#        if not self._words:
#            self.generateWords()
#            
#        return self._words
#        
#    def generateWords(self):
#        "Generate list of words."
#        self._words = F.countDicts([n.words() for n in self.notes])
        
        
    def addNote(self, n):
        self.notes.append(n)
#        self.generateTags()
#        self.generateWords()
        
    def sortNotes(self):
        "Internally sort notes by dates."
        self.notes = sorted(self.notes, key=lambda n: n.date)
        
    def json(self):
        "Returns a json string."

        self.sortNotes()
        j = []
        for n in self.notes:
            j.append({
                "date": n.date,
                "text": n.text}
            )
        print(json.dumps(j, sort_keys=True, indent=4))
            