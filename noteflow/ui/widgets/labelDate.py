#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import noteflow.functions as F

class LabelDate(QLabel):
    
    dateChanged = pyqtSignal(QDate)    
    
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.date = QDate()
        self.calendar = QCalendarWidget()
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.clicked.connect(self.dateChanged)
        self.calendar.clicked.connect(self.setDate)
        self.calendar.clicked.connect(self.calendar.hide)
        
    def setDate(self, date):
        self.date = date
        self.setText(date.toString(Qt.ISODate))
        
    def mouseReleaseEvent(self, event):
        QLabel.mouseReleaseEvent(self, event)
        if self.date:
            self.calendar.setSelectedDate(self.date)
            
            self.calendar.show()
            p = self.parent().mapToGlobal(self.geometry().topRight())
            p = p - QPoint(self.calendar.width(), self.calendar.height())
            self.calendar.move(p)
            