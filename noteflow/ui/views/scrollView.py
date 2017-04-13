#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class scrollView(QScrollArea):
    
    noteSelected = pyqtSignal(int)
    noteActivated = pyqtSignal(int)
    
    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent)
        
    def setNotes(self, notes):
        self.notes = notes
        w = QWidget()
        l = QVBoxLayout(w)
        self.lbls = []
        w.setStyleSheet("background: white;")
        self._loaded = 0
        self.btnLoad = QPushButton("Load more..")
        self.btnLoad.clicked.connect(self.loadItems)
        l.addWidget(self.btnLoad)
        
        self.setWidget(w)
        self.loadItems()
        
    def loadItems(self):
        n = self._loaded
        l = self.widget().layout()
        
        for n in self.notes[n:n+20]:
            lbl = ClickableLabel(n.text)
            lbl.setWordWrap(True)
            lbl.setStatusTip("{} #{}".format(n.date, n.UID))
            lbl.clicked.connect(self.clicked)
            lbl.doubleClicked.connect(self.doubleClicked)
            self.lbls.append(lbl)
            #l.addWidget(edt)
            l.insertWidget(l.count()-1, lbl)
            
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            #l.addWidget(line)
            l.insertWidget(l.count()-1, line)
        
        self._loaded += 20
        if self._loaded >= len(self.notes):
            self.btnLoad.hide()
            
    def clicked(self):
        lbl = self.sender()
        i = self.lbls.index(lbl)
        n = self.notes[i]
        
        for l in self.lbls:
            l.setProperty("selected", False)
            l.style().unpolish(l)
            l.style().polish(l)
        
        lbl.setProperty("selected", True)
        lbl.style().unpolish(lbl)
        lbl.style().polish(lbl)
        
        self.noteSelected.emit(n.UID)
        
    def doubleClicked(self):
        lbl = self.sender()
        i = self.lbls.index(lbl)
        n = self.notes[i]
        self.noteActivated.emit(n.UID)
        
class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()
    
    def __init__(self, text):
        QLabel.__init__(self, text)
        
        self.setStyleSheet("""
            QLabel{
                padding-left: 5px;
            }
            QLabel[selected=true]{
                border-left:3px solid blue;
            }
            """)
        
    def mousePressEvent(self, event):
        QLabel.mousePressEvent(self, event)
        self.clicked.emit()
        
    def mouseDoubleClickEvent(self, event):
        QLabel.mouseDoubleClickEvent(self, event)
        self.doubleClicked.emit()
        