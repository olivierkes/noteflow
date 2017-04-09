#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class tableView(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.notes = []
        self.customTags = []
        
        self.delegate = customDelegate(self)
        self.setItemDelegateForColumn(1, self.delegate)
        
    def setCustomTags(self, tags):
        self.customTags = tags
        self.customTags.tagsChanged.connect(self.customTagsChanged)
        
    def customTagsChanged(self):
        print("FIXME")
        #FIXME
        
    def setupNotes(self, notes):
        if sorted(notes, key=lambda n:n.UID) == \
           sorted(self.notes, key=lambda n:n.UID):
            # Notes haven't changed
            return
        
        self.notes = []
        self.clearContents()    
        self.setRowCount(len(notes))
        y = 0
        self.setSortingEnabled(False)
        for n in notes:
            self.addTblItem(n, y)
            y += 1
        self.setSortingEnabled(True)
        self.sortItems(0)
        
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
                        
        self.notes.append(note)
        
    def addNote(self, note):        
        self.setSortingEnabled(False)
        self.addTblItem(note)
        self.setSortingEnabled(True)
        self.sortItems(0)
        
class customDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self)
        self.parent = parent
        
    def paint(self, painter, option, index):
#        return QStyledItemDelegate.paint(self, painter, option, index)
        self.initStyleOption(option, index)
        ct = self.parent.customTags
        text = option.text
        UID = index.sibling(index.row(), 0).data(Qt.UserRole)
        note = [n for n in self.parent.notes if n.UID == UID][0]
        
        tags = []
        for t in ct:
            if t.match(note):
                tags.append(t)
        
        if not tags:
            # No tag match
            QStyledItemDelegate.paint(self, painter, option, index)
            return
        
        tagsWithBackgrounds = [t for t in tags if t.background or t.border]
        
        M = 4
        h = option.rect.height()
        
        # We reduce the rect for the text
        w = len(tagsWithBackgrounds) * ( h - M + 1)
        option.rect.setRight(option.rect.right() - w)
        # Call the native painter, easier
        QStyledItemDelegate.paint(self, painter, option, index)
        
        # Draw circles for tags with backgrounds
        r = QRect(0, 0, h - 2*M, h - 2*M)
        r.moveTop(option.rect.top() + M)
        r.moveLeft(option.rect.right() + M)
        for t in tagsWithBackgrounds:
            background = t.background if t.background else Qt.transparent  
            border = t.border
            painter.save()
            painter.setBrush(QBrush(background))
            painter.setPen(QPen(border, 2) if border else background)
            #print(t.text, r)
            painter.drawEllipse(r)
            painter.restore()
            r.moveLeft(r.right() + M + 1)   
        