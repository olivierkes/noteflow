#!/usr/bin/env python
# --!-- coding: utf8 --!--

import json, os
import flownote.functions as F
from flownote.models.note import Note
from PyQt5.QtCore import *

EXT = ".txt"

class Notebook(QObject):
    """A collection of notes.

    On the computer, a notebook is a folder containing text files.
    """
    
    noteChanged = pyqtSignal(int)  # param str is the note UID
    
    def __init__(self, name=None, path=None, create=False):
        QObject.__init__(self)
        self.notes = []
        
        if create:
            self.name = name
            self.path = path
            self._content = {}
        
        else:
            # We must load from path
            ini = os.path.join(path, ".FLOWNOTE")
            assert os.path.exists(ini)
            s = QSettings(ini, QSettings.IniFormat)
            self.name = s.value("Name")
            self.path = path
            
            self.load(path)
        
        self.UID = F.uniqueID()
        
    def addNote(self, n):
        self.notes.append(n)
        n.noteChanged.connect(self.noteChanged)
        
    def sortNotes(self):
        "Internally sort notes by dates."
        self.notes = self.sorted(self.notes)
    
    def sorted(self, notes):
        return sorted(notes, key=lambda n: n.date)

#==============================================================================
#   LOAD / SAVE
#==============================================================================
    
    def notesToDisk(self):
        files = {}
        for n in self.notes:
            path = "{y}/{m}/{date}{title}".format(
                y=n.date.split("-")[0],
                m=n.date.split("-")[1],
                date=n.date,
                title="-"+F.slugify(n.title) if n.title else "")
            content = n.toText()
            
            # Make sure no two files have the same path
            n = 2
            nPath = path
            while nPath+EXT in files:
                nPath = "{}_{}".format(path, n)
                n += 1
            path = nPath+EXT
            
            files[path] = content
        return files
        

    def load(self, path):
        
        content = {}
        for root, dirs, files in os.walk(path):
            for f in files:
                if f[-len(EXT):] == EXT:
                    filename = os.path.join(root, f)
                    p = os.path.relpath(filename, path)
                    content[p] = F.loadTextFile(filename)
                    
        self._content = content
        
        for p in content:
            self.addNote(Note(fromText=content[p]))
            

    def save(self):
        print("Saving in: {}".format(self.path))
        
        content = self.notesToDisk()
        oldContent = self._content
        
        # Writing content
        for path in content:
            
            filename = os.path.join(self.path, path)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            if path in oldContent and content[path] == oldContent[path]:
                # Nothing to do, file didn't change
                pass
            
            else:
                # The content of the file changed, or the file is new. We write.
                print("Writing:", path)
                with open(filename, "w", encoding='utf8') as f:
                    f.write(content[path])
                
        # Removing old content
        for path in oldContent:
            if not path in content:
                # We need to remove that file
                filename = os.path.join(self.path, path)
                os.remove(filename)
        
        # Removing empty folders, for the sake of cleanliness
        for root, dirs, files in os.walk(self.path):
            try:
                os.removedirs(root)
            except:
                pass
            
        # Write settings
        filename = os.path.join(self.path, ".FLOWNOTE")
        s = QSettings(filename, QSettings.IniFormat)
        s.setValue("Format", "1")
        s.setValue("Name", self.name)
        
            
        self._content = content