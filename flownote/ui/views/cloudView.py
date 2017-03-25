#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class cloudView(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setSelectionMode(self.ExtendedSelection)
        self.setViewMode(self.IconMode)
        self.setResizeMode(self.Adjust)
        self.setMovement(self.Static)
        self.words = []
        
        self._maxWords = 0
        
    def setWords(self, words):
        self.words = words
        self.clear()
        if not words:
            return
        
        # If there's a limit of number of words
        if self._maxWords > 0:
            val = sorted(words.values())[-self._maxWords]
            words2 = words.copy()
            for w in words2:
                if words2[w] < val:
                    words.pop(w)
        
        minCount, maxCount = min(words.values()), max(words.values())
        if minCount == maxCount:
            minCount -= 1
        minFont, maxFont = 5, 15
        
        for w in words:
            i = QListWidgetItem(w)
            i.setData(Qt.UserRole, words[w])
            f = i.font()
            f.setPointSizeF(minFont + (words[w] - minCount) / (maxCount - minCount) * (maxFont - minFont))
            i.setFont(f)
            self.addItem(i)
        
    def setVisibleWords(self, words):
                
        k = 0
        for k in range(self.count()):
            i = self.item(k)
            if i.text() in words or not words:
                i.setForeground(QBrush())
            else:
                i.setForeground(Qt.gray)
    
    def filterRows(self, text):
        text = text.lower()
        
        k = 0
        for k in range(self.count()):
            i = self.item(k)
            i.setHidden(text not in i.text().lower())