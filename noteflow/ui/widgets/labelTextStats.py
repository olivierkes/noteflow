#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class LabelTextStats(QLabel):  
    
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        
        self.setText("")
        self.hide()
        
        self.words = 0
        self.chars = 0
        self.charsNoSpace = 0
        self.wordsS = 0
        self.charsS = 0
        self.charsNoSpaceS = 0
        
    def setStats(self, words, chars, charsNoSpace, selection=False):
        if not selection:
            self.words = words
            self.chars = chars
            self.charsNoSpace = charsNoSpace
        else:
            self.wordsS = words
            self.charsS = chars
            self.charsNoSpaceS = charsNoSpace
        
        showSel = self.wordsS and (self.words != self.wordsS or 
                                  self.chars != self.charsS or
                                  self.charsNoSpace != self.charsNoSpaceS)
        
        self.setText("<b>{}</b> words / <b>{}</b> chars{}".format(
                     self.words,
                     self.chars,
                     " (<b>{}</b> words / <b>{}</b> chars in selection)".format(
                        self.wordsS, self.charsS) if showSel else ""))
        
        self.setToolTip("<b>{}</b> chars without spaces<br><b>{}</b> pages".format(
            self.charsNoSpace,
            self.words / 250))
        
        self.show()
        
        if self.words == self.chars == 0:
            self.hide()
        
