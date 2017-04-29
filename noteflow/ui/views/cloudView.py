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
        self.customTags = None
        self._customTagsOnly = False
        self._customTagsAlways = False
        self._maxWords = 20
        self._minValue = None
        self._minLength = None

        self.tagMode = False

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
        #self.popup.setWindowFlags(Qt.Popup)
        self.btnSettings.clicked.connect(self.popupMenu)

        self.delegate = customDelegate(self)
        self.setItemDelegate(self.delegate)

    def setTagMode(self, enable):
        self.tagMode = enable
        self.popup.setWord("tags" if enable else "words")

    def mousePressEvent(self, event):
        if Qt.RightButton == event.button():
            self.popupTagMenu(event.pos())
        else:
            return QListWidget.mousePressEvent(self, event)

    def popupTagMenu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return

        from noteflow import MW
        text = item.text()
        m = QMenu(self)

        # Option to hide word. Not for custom tags.
        if not self.customTags or text.lower() not in self.customTags.toListLower():
            a = m.addAction("Hide '{}'".format(text))
            a.triggered.connect(lambda: MW.addToHiddenWords(text))

        if self.tagMode and self.customTags:
            if len(m.actions()):
                m.addSeparator()

            a = m.addAction("Customize {}...".format(text))
            a.triggered.connect(lambda: MW.customizeTag(text))

        m.popup(self.mapToGlobal(pos))

    def setCustomTags(self, tags):
        self.customTags = tags
        self.setTagMode(True if tags else False)
        self.customTags.tagsChanged.connect(self.customTagsChanged)

    def customTagsChanged(self):
        self.update()
        # SizeChange might have changed, so we update them all
        for i in range(self.count()):
            idx = self.indexFromItem(self.item(i))
            self.delegate.sizeHintChanged.emit(idx)

    def setcustomTagsOnly(self, val):
        if val != self._customTagsOnly:
            self._customTagsOnly = val
            self.setWords(self.words)

    def setcustomTagsAlways(self, val):
        if val != self._customTagsAlways:
            self._customTagsAlways = val
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
        p = self.mapToGlobal(self.btnSettings.geometry().center())
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
        if self._minValue:
            words = {w:words[w] for w in words if words[w] >= self._minValue}

        if self._minLength:
            words = {w:words[w] for w in words if len(w) >= self._minLength}

        self.words = words.copy()
        # We store selected items
        selected = [s.text() for s in self.selectedItems()]
        self.blockSignals(True)
        self.clear()
        if not words:
            return

        w2 = {}
        if self._customTagsOnly or self._customTagsAlways:
            cw = self.customTags.toListLower()
            for w in words:
                if w in cw:
                    w2[w] = words[w]

        if not self._customTagsOnly:
            # If there's a limit of number of words
            m = min(self._maxWords, len(self.words))
            w = self.words.copy()
            s = sorted(w, key=w.get)

            while len(w2) < m:
                k = s.pop()
                if not k in w2:
                    w2[k] = w[k]

        words = w2
        minCount = min(words.values())
        maxCount = max(words.values())
        if minCount == maxCount:
            minCount -= 1
        minFont, maxFont = 6, 13

        # Add words to list
        for w in words:
            i = QListWidgetItem(w)
            i.setData(Qt.UserRole, words[w])
            i.setData(Qt.UserRole+1, True)  # Enabled
            i.setToolTip("×{}".format(words[w]))
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
        self._visibleWords = words.copy()
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

from noteflow.ui.views.cloudViewPopup_ui import Ui_CloudViewPopup

class cloudViewPopup(QMenu, Ui_CloudViewPopup):
    def __init__(self, cloud, parent=None, word="words"):
        QMenu.__init__(self, parent)
        self.setupUi(self)
        self.cloud = cloud

        self.setWord(word)
        self.setWindowFlags(Qt.Popup)

        self.sldNWords.valueChanged.connect(self.cloud.setMaxWords)
        self.txtFilter.textChanged.connect(self.cloud.filterRows)
        self.chkCustomOnly.toggled.connect(self.cloud.setcustomTagsOnly)
        self.chkCustomAlways.toggled.connect(self.cloud.setcustomTagsAlways)

    def setWord(self, word):
        self.word = word
        self.lblNbWordsDesc.setText("Number of {} to show:".format(self.word))
        self.chkCustomOnly.setText("Display custom {} only".format(self.word))
        self.chkCustomAlways.setText("Display custom {} always".format(self.word))

    def popup(self):
        n = len(self.cloud.words)
        self.sldNWords.setMaximum(n)
        if self.cloud._maxWords == 0:
            self.sldNWords.setValue(n)
        else:
            self.sldNWords.setValue(self.cloud._maxWords)

        self.chkCustomOnly.setChecked(self.cloud._customTagsOnly)
        self.chkCustomAlways.setChecked(self.cloud._customTagsAlways)
        self.chkCustomOnly.setVisible(self.cloud.customTags is not None)
        self.chkCustomAlways.setVisible(self.cloud.customTags is not None)

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
        cw = self.parent.customTags
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
        cw = self.parent.customTags
        if cw and item.text().lower() in cw.toListLower():
            tag = cw.find(item.text())

            enabled = index.data(Qt.UserRole+1)
            color = tag.color if tag.color else QColor("#000")
            color.setAlpha(255 if enabled else 64)
            if tag.background:
                background = tag.background
                background.setAlpha(255 if enabled else 64)
            else:
                background = Qt.transparent
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

            if background or border:
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


