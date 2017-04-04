#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class noteEdit(QTextEdit):
    
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.note = None
        self.textChanged.connect(self.updateNote)
        self.setEnabled(False)
        
    def setNote(self, note):
        if note is not None:
            self.note = note
            self.setText(note.text)
            self.setEnabled(True)
        else:
            self.note = None
            self.setEnabled(False)
            self.setText("")
            
        
    def updateNote(self):
        if self.note:
            self.note.setText(self.toPlainText())
        else:
            if self.toPlainText():
                self.setText("")
            self.setEnabled(False)