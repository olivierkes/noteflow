#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from noteflow.ui.views.noteCompleter_ui import Ui_noteCompleter
from noteflow.models.note import Note

class noteCompleter(QWidget, Ui_noteCompleter):
    activated = pyqtSignal(Note)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Popup)
        self.text.textChanged.connect(self.updateListFromData)
        self.text.returnPressed.connect(self.submit)
        self.listDelegate = listCompleterDelegate(self)
        self.list.setItemDelegate(self.listDelegate)
        self.list.itemClicked.connect(self.submit)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hide()

    def popup(self, completion=""):
        self.updateListFromData()
        self.text.setText(completion)
        self.text.setFocus(Qt.PopupFocusReason)
        self.show()

    def addCategory(self, title):
        item = QListWidgetItem(title)
        item.setBackground(QBrush(QColor("#AAAAFF")))
        item.setForeground(QBrush(QColor("#1111FF")))
        item.setFlags(Qt.ItemIsEnabled)
        self.list.addItem(item)

    def updateListFromData(self):
        self.list.clear()

        from noteflow import MW
        for nb in MW.notebooks:
            # Filter notes
            text = self.text.text()
            filtered = nb.notes
            for w in text.split(" "):
                w = w.strip()
                if "#" in w:
                    filtered = [n for n in filtered if w in n.text]
                else:
                    filtered = [n for n in filtered if w in n.title]
            if filtered:
                self.addCategory(nb.name)
                for n in sorted(filtered, key=lambda n:n.date):
                    i = QListWidgetItem(n.title)
                    i.setData(Qt.UserRole, n.UID)
                    i.setData(Qt.UserRole + 1, n.date)
                    self.list.addItem(i)

        self.list.setCurrentRow(1)
        self.text.setFocus(Qt.PopupFocusReason)

    def submit(self):
        i = self.list.currentItem()
        UID = i.data(Qt.UserRole)
        from noteflow import MW
        note = MW.noteFromUID(UID)
        self.activated.emit(note)
        self.hide()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Up, Qt.Key_Down]:
            self.list.keyPressEvent(event)
        else:
            QWidget.keyPressEvent(self, event)


class listCompleterDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        extra = index.data(Qt.UserRole + 1)
        if not extra:
            return QStyledItemDelegate.paint(self, painter, option, index)

        else:
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.color(QPalette.Inactive, QPalette.Highlight))

            title = index.data()
            extra = " - {}".format(extra)
            painter.drawText(option.rect, Qt.AlignLeft, title)

            fm = QFontMetrics(option.font)
            w = fm.width(title)
            r = QRect(option.rect)
            r.setLeft(r.left() + w)
            painter.save()
            painter.setPen(QColor("#777"))
            # if option.state & QStyle.State_Selected:
            #     painter.setPen(QColor(S.highlightedTextLight))
            # else:
            #     painter.setPen(QColor(S.textLight))

            painter.drawText(r, Qt.AlignLeft, extra)
            painter.restore()
