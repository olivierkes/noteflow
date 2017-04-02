#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class noteEdit(QTextEdit):
    
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.note = None
        
        self.document().contentsChanged.connect(self.updateNote)
        
    def setNote(self, note):
        self.note = note
        self.setText(note.text)
        
    def updateNote(self):
        if self.note:
            self.note.setText(self.toPlainText())