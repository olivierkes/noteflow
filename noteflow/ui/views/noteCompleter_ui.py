# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'noteflow/ui/views/noteCompleter_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_noteCompleter(object):
    def setupUi(self, noteCompleter):
        noteCompleter.setObjectName("noteCompleter")
        noteCompleter.resize(517, 182)
        self.verticalLayout = QtWidgets.QVBoxLayout(noteCompleter)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = QtWidgets.QLineEdit(noteCompleter)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.list = QtWidgets.QListWidget(noteCompleter)
        self.list.setObjectName("list")
        self.verticalLayout.addWidget(self.list)

        self.retranslateUi(noteCompleter)
        QtCore.QMetaObject.connectSlotsByName(noteCompleter)

    def retranslateUi(self, noteCompleter):
        _translate = QtCore.QCoreApplication.translate
        noteCompleter.setWindowTitle(_translate("noteCompleter", "Form"))

