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
        self._visibleWords = []
        self.customWords = None
        self._customWordsOnly = False
        self._customWordsAlways = False
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
        
        self.delegate = customDelegate(self)
        self.setItemDelegate(self.delegate)
        
    def setCustomTags(self, tags):
        self.customWords = tags
        self.customWords.tagsChanged.connect(self.customTagsChanged)
        
    def customTagsChanged(self):
        print("FIXME")
        #FIXME
        
    def setCustomWordsOnly(self, val):
        if val != self._customWordsOnly:
            self._customWordsOnly = val
            self.setWords(self.words)
        
    def setCustomWordsAlways(self, val):
        if val != self._customWordsAlways:
            self._customWordsAlways = val
            self.setWords(self.words)
        
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
        # We store selected items
        selected = [s.text() for s in self.selectedItems()]
        self.blockSignals(True)
        self.clear()
        if not words:
            return
        
        w2 = {}
        if self._customWordsOnly or self._customWordsAlways:
            cw = self.customWords.toListLower()
            for w in words:
                if w in cw:
                    w2[w] = words[w]
        
        if not self._customWordsOnly:
            # If there's a limit of number of words
            m = min(self._maxWords, len(self.words))
            w = self.words.copy()
            s = sorted(w, key=w.get)
            
            while len(w2) < m:
                k = s.pop()
                if not k in w2:
                    w2[k] = w[k]
        
        words = w2
        minCount, maxCount = min(words.values()), max(words.values())
        if minCount == maxCount:
            minCount -= 1
        minFont, maxFont = 6, 13
        
        # Add words to list
        for w in words:
            i = QListWidgetItem(w)
            i.setData(Qt.UserRole, words[w])
            i.setData(Qt.UserRole+1, True)  # Enabled
            f = i.font()
            f.setPointSizeF(minFont + (words[w] - minCount) / (maxCount - minCount) * (maxFont - minFont))
            i.setFont(f)    
            self.addItem(i)
            
        self.setVisibleWords(self._visibleWords)
        
        # Reselect items
        [self.item(r).setSelected(True) for r in range(self.count()) if self.item(r).text() in selected]
        
        self.updateGeometry()
        self.blockSignals(False)
        
    def setVisibleWords(self, words):
        self._visibleWords = words
        k = 0
        for k in range(self.count()):
            i = self.item(k)
            if i.text().lower() in words or not words:
                i.setForeground(QBrush())                
                i.setData(Qt.UserRole+1, True)
            else:
                i.setForeground(Qt.gray)                
                i.setData(Qt.UserRole+1, False)
    
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
        self.chkCustomAlways.setText("Display custom {} always".format(self.word))
        
        self.sldNWords.valueChanged.connect(self.cloud.setMaxWords)
        self.txtFilter.textChanged.connect(self.cloud.filterRows)
        self.chkCustomOnly.toggled.connect(self.cloud.setCustomWordsOnly)
        self.chkCustomAlways.toggled.connect(self.cloud.setCustomWordsAlways)
        
    def popup(self):
        n = len(self.cloud.words)
        self.sldNWords.setMaximum(n)
        if self.cloud._maxWords == 0:
            self.sldNWords.setValue(n)
        else:
            self.sldNWords.setValue(self.cloud._maxWords)
        
        self.chkCustomOnly.setChecked(self.cloud._customWordsOnly)
        self.chkCustomAlways.setChecked(self.cloud._customWordsAlways)
        self.chkCustomOnly.setVisible(self.cloud.customWords is not None)
        self.chkCustomAlways.setVisible(self.cloud.customWords is not None)
        
        self.show()
        
class customDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self)
        self.parent = parent
        self.margin = 2
        self.padding = 1
        
    def sizeHint(self, option, index):
        self.initStyleOption(option, index)
        item = self.parent.item(index.row())
        cw = self.parent.customWords
        tag = None;
        if cw and item.text().lower() in cw.toListLower():
            tag = cw.find(item.text())
            option.text = tag.text
            
        s = qApp.style().sizeFromContents(QStyle.CT_ItemViewItem, option, QSize())
        
        if tag:
            s = s + QSize(2*self.margin + 2*self.padding, 2*self.margin + 2*self.padding)
        return s
        
        
    def paint(self, painter, option, index):
#        return QStyledItemDelegate.paint(self, painter, option, index)
        self.initStyleOption(option, index)
        item = self.parent.item(index.row())
        cw = self.parent.customWords
        if cw and item.text().lower() in cw.toListLower():
            tag = cw.find(item.text())
            
            enabled = index.data(Qt.UserRole+1)
            color = tag.color if tag.color else QColor("#000")
            color.setAlpha(255 if enabled else 64)
            background = tag.background if tag.background else QColor()            
            background.setAlpha(255 if enabled else 64)
            border = None
            if tag.border:
                border = tag.border
                border.setAlpha(255 if enabled else 64)
            
            # Selection
            cg = QPalette.ColorGroup(QPalette.Normal if option.state & QStyle.State_Enabled else QPalette.Disabled)
            if cg == QPalette.Normal and not option.state & QStyle.State_Active:
                cg = QPalette.Inactive
    
            if option.state & QStyle.State_Selected:
                painter.save()
                painter.setBrush(option.palette.brush(cg, QPalette.Highlight))
                painter.setPen(Qt.NoPen)
                painter.drawRect(option.rect)
                painter.restore()
                
            option.rect = option.rect.adjusted(self.margin, self.margin, -self.margin, -self.margin)
            
            if tag.background:
                painter.save()
                painter.setBrush(QBrush(background))
                painter.setPen(QPen(border, 2) if border else Qt.transparent)
                painter.drawRoundedRect(option.rect, 8, 8)
                painter.restore()
            
            painter.save()  
            painter.setFont(option.font)
            painter.setPen(color)
            painter.drawText(option.rect, Qt.AlignVCenter | Qt.AlignHCenter, tag.text)
            painter.restore()
            
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
        
        