#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from noteflow.ui.widgets.folderDialog_ui import Ui_folderDialog
import noteflow.functions as F

class folderDialog(QDialog, Ui_folderDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        for c in range(1, self.model.columnCount()):
            self.tree.setColumnHidden(c, True)
        
        self.tree.selectionModel().selectionChanged.connect(self.checkValiditySel)
        
        startPath = F.appPath()
        #startPath = QDir.homePath()
        index = self.model.index(startPath, 0)
        self.tree.setCurrentIndex(index)
        self.tree.setExpanded(index, True)
        self.tree.scrollTo(index, self.tree.PositionAtTop)
        self.checkValidity(index)
        
    def checkValiditySel(self, sel):
        index = sel.indexes()[0]
        self.checkValidity(index)
        
    def checkValidity(self, index):
        path = self.model.filePath(index)
        filename = os.path.join(path, ".NOTEFLOW")
        valid = os.path.exists(filename)
        self.btns.button(self.btns.Open).setEnabled(valid)
        self.label.setVisible(not valid)
        
        self.result = path if valid else ""
