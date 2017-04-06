#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class tableView(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self._notesInTable = None
        self.customTags = None
        
    def setCustomTags(self, tags):
        self.customTags = tags
        self.customTags.tagsChanged.connect(self.customTagsChanged)
        
    def customTagsChanged(self):
        print("FIXME")
        #FIXME
        
    def setupNotes(self, notes):
        if notes == self._notesInTable:
            # Notes haven't changed
            return
                    
        self.clearContents()    
        self.setRowCount(len(notes))
        y = 0
        self.setSortingEnabled(False)
        for n in notes:
            self.addTblItem(n, y)
            y += 1
        self.setSortingEnabled(True)
        self.sortItems(0)
        self._notesInTable = notes
        
    def addTblItem(self, note, y=None):
        f = qApp.font()
        f.setPointSize(f.pointSize() * .8)
        
        if y is None:
            y = self.rowCount()
            self.setRowCount(y+1)
        
        i = QTableWidgetItem(note.date)
        i.setData(Qt.UserRole, note.UID)
        i.setForeground(Qt.darkGray)
        i.setFont(f)
        self.setItem(y, 0, i)
        item = QTableWidgetItem(note.title or note.text[:50])
        self.setItem(y, 1, item)
        self.setItem(y, 2, QTableWidgetItem(str(note.UID)))
        
        # Check custom tags
        if self.customTags:
            for t in self.customTags:
                if t.match(note):
                    if t.color:
                        item.setForeground(QBrush(t.color))
                    if t.background:
                        item.setBackground(QBrush(t.background))
        
    def addNote(self, note):        
        self.setSortingEnabled(False)
        self.addTblItem(note)
        self.setSortingEnabled(True)
        self.sortItems(0)