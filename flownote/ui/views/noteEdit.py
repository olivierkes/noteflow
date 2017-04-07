#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from flownote.ui.views.markdownHighlighter import MarkdownHighlighter

class noteEdit(QTextEdit):
    
    def __init__(self, parent=None, highlighting=True):
        QTextEdit.__init__(self, parent)
        self.note = None
        self.textChanged.connect(self.updateNote)
        self.setEnabled(False)
        
        self.highlighter = None
        if highlighting:
            self.highlighter = MarkdownHighlighter(self)
            self.highlighter.setColorScheme(
                QColor(Qt.black),
                QColor(Qt.white),
                QColor(Qt.black),
                QColor(Qt.blue),
                QColor(Qt.red)
            )
        
    def setNote(self, note):
        if note is not None:
            self.note = note
            self.setText(note.wholeText())
            self.setEnabled(True)
        else:
            self.note = None
            self.setEnabled(False)
            self.setText("")
            
        
    def updateNote(self):
        if self.note:
            self.note.setWholeText(self.toPlainText())
        else:
            if self.toPlainText():
                self.setText("")
            self.setEnabled(False)
            
    def setHighlighted(self, words, tags):
        if self.highlighter:
            pass
            #FIXME
            # self.highlighter.setHighlighted(words, tags)