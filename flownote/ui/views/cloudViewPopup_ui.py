# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flownote/ui/views/cloudViewPopup_ui.ui'
#
# Created: Thu Mar 30 17:20:25 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CloudViewPopup(object):
    def setupUi(self, CloudViewPopup):
        CloudViewPopup.setObjectName("CloudViewPopup")
        CloudViewPopup.resize(239, 89)
        self.formLayout = QtWidgets.QFormLayout(CloudViewPopup)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)
        self.formLayout.setObjectName("formLayout")
        self.lblNbWordsDesc = QtWidgets.QLabel(CloudViewPopup)
        self.lblNbWordsDesc.setObjectName("lblNbWordsDesc")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblNbWordsDesc)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sldNWords = QtWidgets.QSlider(CloudViewPopup)
        self.sldNWords.setMinimum(1)
        self.sldNWords.setOrientation(QtCore.Qt.Horizontal)
        self.sldNWords.setObjectName("sldNWords")
        self.horizontalLayout.addWidget(self.sldNWords)
        self.lblNbWords = QtWidgets.QLabel(CloudViewPopup)
        self.lblNbWords.setObjectName("lblNbWords")
        self.horizontalLayout.addWidget(self.lblNbWords)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.chkCustomFirst = QtWidgets.QCheckBox(CloudViewPopup)
        self.chkCustomFirst.setObjectName("chkCustomFirst")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.chkCustomFirst)
        self.chkCustomOnly = QtWidgets.QCheckBox(CloudViewPopup)
        self.chkCustomOnly.setObjectName("chkCustomOnly")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.chkCustomOnly)
        self.txtFilter = QtWidgets.QLineEdit(CloudViewPopup)
        self.txtFilter.setObjectName("txtFilter")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.txtFilter)

        self.retranslateUi(CloudViewPopup)
        self.sldNWords.valueChanged['int'].connect(self.lblNbWords.setNum)
        QtCore.QMetaObject.connectSlotsByName(CloudViewPopup)

    def retranslateUi(self, CloudViewPopup):
        _translate = QtCore.QCoreApplication.translate
        CloudViewPopup.setWindowTitle(_translate("CloudViewPopup", "Form"))
        self.lblNbWordsDesc.setText(_translate("CloudViewPopup", "Number of words to show:"))
        self.lblNbWords.setText(_translate("CloudViewPopup", "1"))
        self.chkCustomFirst.setText(_translate("CloudViewPopup", "Display custom words first"))
        self.chkCustomOnly.setText(_translate("CloudViewPopup", "Display custom words only"))

