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
        
        self.path = None
        
    def addNote(self, n):
        self.notes.append(n)
        
    def sortNotes(self):
        "Internally sort notes by dates."
        self.notes = self.sorted(self.notes)
    
    def sorted(self, notes):
        return sorted(notes, key=lambda n: n.date)
        
    def json(self, notes=None):
        "Returns a json string for the given notes, or all notes if notes is None."
        if notes is None:
            notes = self.notes

        notes = self.sorted(notes)

        j = []
        for n in notes:
            j.append({
                "date": n.date,
                "text": n.text}
            )
        return json.dumps(j, sort_keys=True, indent=4)
        
    def save(self):
        # Order notes
        self.notes = self.sorted(self.notes)
        
        def saveNotes(notes, y):
            print(self.json(notes))
            print("{}: {} notes.".format(y, len(notes)))
        
        def splitNotes(f):
            collection = {}
            for n in self.notes:
                d = f(n)
                if d not in collection:
                    collection[d] = [n for n in self.notes if f(n) == d]
            
            return collection
        
        # Yearly
        #collection = splitNotes(lambda n:n.date.split("-")[0])
        
        # Monthly
        collection = splitNotes(lambda n:"-".join(n.date.split("-")[:2]))
        
        # Daily
        #collection = splitNotes(lambda n:n.date)
        
        for c in collection:
            saveNotes(collection[c], c)
         