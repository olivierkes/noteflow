#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import re

from noteflow.ui.views.markdownHighlighter import MarkdownHighlighter as MH
from noteflow.ui.views.markdownEnums import MarkdownState as MS

class structureView(QTreeWidget):

    AtxRegExp = re.compile(r"^#+\s*(.+?)\s*#*$")
    navigateToPosition = pyqtSignal(int)

    def __init__(self, parent=None):
        QTreeWidget.__init__(self, parent)
        self.note = None

        self.setHeaderHidden(True)
        self.setStyleSheet("background:transparent;")

        self.itemClicked.connect(self.expandItem)
        self.itemClicked.connect(self.navigateTo)

    def setNote(self, note):
        self.note = note
        self.updateStructure()

    def updateStructure(self):
        self.clear()
        editor = self.sender()
        block = editor.document().firstBlock()
        currentBlock = editor.textCursor().block()
        currentItem = None

        parent = self.invisibleRootItem()
        parent.__level = -1
        while block.isValid():

            if self.isHeading(block):
                level, text = self.getHeadingData(block)

                # get parent level
                while parent.__level >= level:
                    parent = parent.parent() or self.invisibleRootItem()

                child = QTreeWidgetItem(parent, [text])
                child.__level = level
                child.__pos = block.position()

                parent = child

            if block == currentBlock:
                currentItem = parent

            block = block.next()

        self.setCurrentItem(currentItem)
        self.expandItem(currentItem)
        self.scrollToItem(currentItem, self.PositionAtTop)

    def navigateTo(self, item, column):
        self.navigateToPosition.emit(item.__pos)

    def isHeading(self, block):
        return MH.isHeadingBlockState(block.userState())

    def getHeadingData(self, block):
        state = block.userState()
        if state in [
                MS.MarkdownStateAtxHeading1,
                MS.MarkdownStateAtxHeading2,
                MS.MarkdownStateAtxHeading3,
                MS.MarkdownStateAtxHeading4,
                MS.MarkdownStateAtxHeading5,
                MS.MarkdownStateAtxHeading6,
            ]:
            level = state - MS.MarkdownStateAtxHeading1
            r = self.AtxRegExp
            text = r.match(block.text()).group(1)

        elif state == MS.MarkdownStateSetextHeading1Line1:
            text = block.text()
            level = 0

        elif state == MS.MarkdownStateSetextHeading2Line1:
            text = block.text()
            level = 1

        return level, text
