#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from noteflow.ui.widgets.preferences_ui import Ui_Preferences
import noteflow.functions as F


class Preferences(QDialog, Ui_Preferences):
    def __init__(self, MW, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        ## Connections
        # General
        self.chkOpenLast.stateChanged.connect(
            lambda: F.settings().setValue("OpenLast", self.chkOpenLast.checkState()))

        #Words
        self.spnWordsMinSize.valueChanged.connect(MW.setMinWordSize)
        self.txtWordsExclude.editingFinished.connect(self.setWordsExclude)

        # Tags
        self.tags = MW.tags
        self.btnColor.clicked.connect(lambda: self.setColor("color", -1))
        self.btnTextColor.clicked.connect(lambda: self.setColor("text", -1))
        self.btnBorderColor.clicked.connect(lambda: self.setColor("border", -1))

        self.btnClearColor.clicked.connect(lambda: self.setColor("color", None))
        self.btnClearTextColor.clicked.connect(lambda: self.setColor("text", None))
        self.btnClearBorderColor.clicked.connect(lambda: self.setColor("border", None))
        
        self.btnTagRemove.clicked.connect(self.removeTag)
        self.btnTagRemove.setEnabled(False)
        
        self.delegate = tagDelegate(self)
        self.lstTags.setItemDelegate(self.delegate)
        f = self.lstTags.font()
        f.setPointSize(11)
        self.lstTags.setFont(f)

        self.lstTags.currentTextChanged.connect(self.setCurrentTag)

    def showEvent(self, event):
        from noteflow import MW
        # Center window
        c = MW.geometry().center()
        s = self.size()
        self.move(c - QPoint(s.width() / 2, s.height() / 2))

    def loadValues(self):
        from noteflow import MW

        # General
        self.chkOpenLast.setCheckState(F.settings("OpenLast", Qt.Checked, int))

        # Clouds
        self.spnWordsMinSize.setValue(MW.minWordSize)
        self.txtWordsExclude.setText(", ".join(MW.hiddenWords))

        # Custom tags
        text = ""
        if self.lstTags.currentItem():
            text = self.lstTags.currentItem().text()
        
        self.lstTags.blockSignals(True)
        self.lstTags.clear()
        for t in MW.tags:
            self.lstTags.addItem(t.text)
        self.lstTags.blockSignals(False)

        if text:
            items = self.lstTags.findItems(text, Qt.MatchExactly)
            if items:
                self.lstTags.setCurrentItem(items[0])

    def setWordsExclude(self):
        from noteflow import MW
        words = self.txtWordsExclude.text().split(", ")
        words = [w.strip().lower() for w in words if w]
        MW.setHiddenWords(words)

#==============================================================================
#   TAGS
#==============================================================================

    def removeTag(self):
        if not self.lstTags.currentItem():
            return

        tag = self.lstTags.currentItem().text()
        self.tags.removeTag(tag)
        self.setCurrentTag()

    def setCurrentTag(self, text=""):
        tag = self.tags.find(text)
        if tag is None:
            self.lblTag.setText("")
            self.setColor("color", None)
            self.setColor("text", None)
            self.setColor("border", None)
            self.btnTagRemove.setEnabled(False)
            return
        
        self.btnTagRemove.setEnabled(True)
        self.tag = tag
        self.lblTag.setText(tag.text)

        tag.blockSignals(True)
        self.setColor("color", tag.background)
        self.setColor("text", tag.color)
        self.setColor("border", tag.border)
        tag.blockSignals(False)
        
        self.lstTags.blockSignals(True)
        item = self.lstTags.findItems(text, Qt.MatchFixedString)[0]
        self.lstTags.setCurrentItem(item)
        self.lstTags.blockSignals(False)
    
    def getColor(self):
        color = Qt.white # default color
        self.colorDialog = QColorDialog(color, self)
        color = self.colorDialog.getColor(color)
        if color.isValid():
            return color

    def setColor(self, which, color=None):
        if color == -1:
            color = self.getColor()
            if not color: 
                return

        btn = {
            "color" : self.btnColor,
            "text"  : self.btnTextColor,
            "border": self.btnBorderColor,
            }[which]

        if color:
            btn.setStyleSheet("background-color: {}".format(color.name()))
        else:
            btn.setStyleSheet("")

        if which == "color":
            self.tag.background = color
        elif which == "text":
            self.tag.color = color
        elif which == "border":
            self.tag.border = color
        
        self.tag.changed.emit()
    
class tagDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self)
        self.parent = parent
        self.tags = parent.tags
        self.margin = 2
        self.padding = 10

    def sizeHint(self, option, index):
        self.initStyleOption(option, index)
        text = option.text

        tag = None;
        if text.lower() in self.tags.toListLower():
            tag = self.tags.find(text)
            option.text = tag.text

        s = qApp.style().sizeFromContents(QStyle.CT_ItemViewItem, option, QSize())

        if tag:
            s = s + QSize(2*self.margin + 2*self.padding, 2*self.margin + 2*self.padding)
        return s

    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        text = option.text
        if self.tags and text.lower() in self.tags.toListLower():
            tag = self.tags.find(text)

            color = tag.color if tag.color else QColor("#000")
            if tag.background:
                background = tag.background
            else:
                background = Qt.transparent
            border = None
            if tag.border:
                border = tag.border

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

            if background or border:
                painter.save()
                painter.setBrush(QBrush(background))
                painter.setPen(QPen(border, 2) if border else Qt.transparent)
                painter.drawRoundedRect(option.rect, 14, 14)
                painter.restore()

            painter.save()
            painter.setFont(option.font)
            painter.setPen(color)
            painter.drawText(option.rect, Qt.AlignVCenter | Qt.AlignHCenter, tag.text)
            painter.restore()

        else:
            QStyledItemDelegate.paint(self, painter, option, index)