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
        
        sp = self.sizePolicy()
        sp.setVerticalPolicy(QSizePolicy.Preferred)
        self.setSizePolicy(sp)
        
        self.words = []
        
        self._maxWords = 20
        
        # Setting button
        self.btnSettings = QPushButton(QIcon.fromTheme("applications-system"), "", self)
        self.btnSettings.setGeometry(QRect(0, 0, 16, 16))
        self.btnSettings.setMinimumSize(QSize(16, 16))
        self.btnSettings.setMaximumSize(QSize(16, 16))
        self.btnSettings.setFlat(True)
        self.btnSettings.setObjectName("btnSettings")
        self.btnSettings.hide()
        #self.btnSettings.installEventFilter(self)
        #self.btnSettings.clicked.connect(self.split)
        
        self.popup = cloudViewPopup(cloud=self, word="words")
        self.popup.setWindowFlags(Qt.Popup)
        self.btnSettings.clicked.connect(self.popupMenu)
        
    def enterEvent(self, event):
        QListWidget.enterEvent(self, event)
        self.btnSettings.show()
        
    def leaveEvent(self, event):
        QListWidget.leaveEvent(self, event)
        self.btnSettings.hide()
        
    
        
    def sizeHint(self):
        r = QRect()
        for i in range(self.count()):
            item = self.item(i)
            r = r.united(self.visualItemRect(item))
        s = r.size()
        s.setHeight(s.height() + 2 * self.frameWidth())
        return s
        
    def popupMenu(self):
        p = self.btnSettings.parent().mapToGlobal(self.btnSettings.geometry().bottomRight())
        r = QRect(p, QSize(150, 30))
        self.popup.setGeometry(r)
        self.popup.popup()
        
    def setMaxWords(self, maxWords):
        if maxWords != self._maxWords:
            self._maxWords = maxWords
            self.setWords(self.words)
        
    def resizeEvent(self, event):
        QListWidget.resizeEvent(self, event)
        # Adjust the setting button position
        self.btnSettings.move(self.width() - 16, 0)
        self.updateGeometry()
        
    def setWords(self, words):
        self.words = words.copy()
        self.clear()
        if not words:
            return
        
        # If there's a limit of number of words
        if self._maxWords > 0:
            m = min(self._maxWords, len(words))
            val = sorted(words.values())[-m]
            words2 = words.copy()
            for w in words2:
                if words2[w] < val:
                    words.pop(w)
        
        minCount, maxCount = min(words.values()), max(words.values())
        if minCount == maxCount:
            minCount -= 1
        minFont, maxFont = 6, 13
        
        for w in words:
            i = QListWidgetItem(w)
            i.setData(Qt.UserRole, words[w])
            f = i.font()
            f.setPointSizeF(minFont + (words[w] - minCount) / (maxCount - minCount) * (maxFont - minFont))
            i.setFont(f)
            self.addItem(i)
            
        self.updateGeometry()
        
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
            
from flownote.ui.views.cloudViewPopup_ui import Ui_CloudViewPopup

class cloudViewPopup(QWidget, Ui_CloudViewPopup):
    def __init__(self, cloud, parent=None, word="words"):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.cloud = cloud
        
        self.word = word
        self.lblNbWordsDesc.setText("Number of {} to show:".format(self.word))
        self.chkCustomOnly.setText("Display custom {} only".format(self.word))
        self.chkCustomFirst.setText("Display custom {} first".format(self.word))
        
        self.sldNWords.valueChanged.connect(self.cloud.setMaxWords)
        self.txtFilter.textChanged.connect(self.cloud.filterRows)
        
    def popup(self):
        n = len(self.cloud.words)
        self.sldNWords.setMaximum(n)
        if self.cloud._maxWords == 0:
            self.sldNWords.setValue(n)
        else:
            self.sldNWords.setValue(self.cloud._maxWords)
        
        self.show()
        