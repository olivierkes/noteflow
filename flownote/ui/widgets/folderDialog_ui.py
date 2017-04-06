# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flownote/ui/dialogs/folderDialog_ui.ui'
#
# Created: Sun Apr  2 15:48:36 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_folderDialog(object):
    def setupUi(self, folderDialog):
        folderDialog.setObjectName("folderDialog")
        folderDialog.resize(437, 445)
        self.verticalLayout = QtWidgets.QVBoxLayout(folderDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree = QtWidgets.QTreeView(folderDialog)
        self.tree.setObjectName("tree")
        self.verticalLayout.addWidget(self.tree)
        self.label = QtWidgets.QLabel(folderDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btns = QtWidgets.QDialogButtonBox(folderDialog)
        self.btns.setOrientation(QtCore.Qt.Horizontal)
        self.btns.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Open)
        self.btns.setObjectName("btns")
        self.verticalLayout.addWidget(self.btns)

        self.retranslateUi(folderDialog)
        self.btns.accepted.connect(folderDialog.accept)
        self.btns.rejected.connect(folderDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(folderDialog)

    def retranslateUi(self, folderDialog):
        _translate = QtCore.QCoreApplication.translate
        folderDialog.setWindowTitle(_translate("folderDialog", "Dialog"))
        self.label.setText(_translate("folderDialog", "Please select a valid existant flownote folder."))

