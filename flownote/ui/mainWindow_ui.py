# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flownote/ui/mainWindow_ui.ui'
#
# Created: Tue Apr  4 23:25:05 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 779)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.wdgTab = QtWidgets.QWidget(self.centralwidget)
        self.wdgTab.setObjectName("wdgTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.wdgTab)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tab = QTabBar(self.wdgTab)
        self.tab.setObjectName("tab")
        self.verticalLayout_5.addWidget(self.tab)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_5.addWidget(self.wdgTab)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(6)
        self.splitter.setObjectName("splitter")
        self.filter = QtWidgets.QWidget(self.splitter)
        self.filter.setObjectName("filter")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.filter)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wdgCalendar = QtWidgets.QWidget(self.filter)
        self.wdgCalendar.setObjectName("wdgCalendar")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.wdgCalendar)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.calendar = QtWidgets.QCalendarWidget(self.wdgCalendar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar.setNavigationBarVisible(True)
        self.calendar.setDateEditEnabled(True)
        self.calendar.setObjectName("calendar")
        self.verticalLayout_7.addWidget(self.calendar)
        self.wdgDateInfos = QtWidgets.QWidget(self.wdgCalendar)
        self.wdgDateInfos.setObjectName("wdgDateInfos")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.wdgDateInfos)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txtDate = QtWidgets.QLineEdit(self.wdgDateInfos)
        self.txtDate.setFrame(False)
        self.txtDate.setReadOnly(True)
        self.txtDate.setObjectName("txtDate")
        self.horizontalLayout_4.addWidget(self.txtDate)
        self.btnDateClear = QtWidgets.QPushButton(self.wdgDateInfos)
        self.btnDateClear.setText("")
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.btnDateClear.setIcon(icon)
        self.btnDateClear.setFlat(True)
        self.btnDateClear.setObjectName("btnDateClear")
        self.horizontalLayout_4.addWidget(self.btnDateClear)
        self.verticalLayout_7.addWidget(self.wdgDateInfos)
        self.verticalLayout_2.addWidget(self.wdgCalendar)
        self.widget = QtWidgets.QWidget(self.filter)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lstTags = cloudView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstTags.sizePolicy().hasHeightForWidth())
        self.lstTags.setSizePolicy(sizePolicy)
        self.lstTags.setObjectName("lstTags")
        self.verticalLayout_4.addWidget(self.lstTags)
        self.lstWords = cloudView(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstWords.sizePolicy().hasHeightForWidth())
        self.lstWords.setSizePolicy(sizePolicy)
        self.lstWords.setObjectName("lstWords")
        self.verticalLayout_4.addWidget(self.lstWords)
        self.verticalLayout_2.addWidget(self.widget)
        self.grpNotes = QtWidgets.QWidget(self.filter)
        self.grpNotes.setObjectName("grpNotes")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.grpNotes)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.txtFilter = QtWidgets.QLineEdit(self.grpNotes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtFilter.sizePolicy().hasHeightForWidth())
        self.txtFilter.setSizePolicy(sizePolicy)
        self.txtFilter.setClearButtonEnabled(True)
        self.txtFilter.setObjectName("txtFilter")
        self.verticalLayout_3.addWidget(self.txtFilter)
        self.tblList = QtWidgets.QTableWidget(self.grpNotes)
        self.tblList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tblList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblList.setShowGrid(False)
        self.tblList.setWordWrap(False)
        self.tblList.setObjectName("tblList")
        self.tblList.setColumnCount(3)
        self.tblList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblList.setHorizontalHeaderItem(2, item)
        self.tblList.horizontalHeader().setVisible(False)
        self.tblList.horizontalHeader().setMinimumSectionSize(1)
        self.tblList.verticalHeader().setVisible(False)
        self.tblList.verticalHeader().setDefaultSectionSize(20)
        self.verticalLayout_3.addWidget(self.tblList)
        self.verticalLayout_2.addWidget(self.grpNotes)
        self.editor = QtWidgets.QStackedWidget(self.splitter)
        self.editor.setObjectName("editor")
        self.editorPage1 = QtWidgets.QWidget()
        self.editorPage1.setObjectName("editorPage1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.editorPage1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = noteEdit(self.editorPage1)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtNoteTitle = QtWidgets.QLineEdit(self.editorPage1)
        self.txtNoteTitle.setObjectName("txtNoteTitle")
        self.horizontalLayout_3.addWidget(self.txtNoteTitle)
        self.noteDate = QtWidgets.QDateEdit(self.editorPage1)
        self.noteDate.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.noteDate.setCalendarPopup(True)
        self.noteDate.setObjectName("noteDate")
        self.horizontalLayout_3.addWidget(self.noteDate)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.editor.addWidget(self.editorPage1)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scroll = scrollView(self.page)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_6.addWidget(self.scroll)
        self.editor.addWidget(self.page)
        self.horizontalLayout_5.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 20))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menuNote = QtWidgets.QMenu(self.menubar)
        self.menuNote.setObjectName("menuNote")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actOpenNotebook = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("folder-open")
        self.actOpenNotebook.setIcon(icon)
        self.actOpenNotebook.setObjectName("actOpenNotebook")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("preferences-system")
        self.actionPreferences.setIcon(icon)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.actQuit.setIcon(icon)
        self.actQuit.setObjectName("actQuit")
        self.actCloseCurrent = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("window-close")
        self.actCloseCurrent.setIcon(icon)
        self.actCloseCurrent.setObjectName("actCloseCurrent")
        self.actNewNotebook = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("folder-new")
        self.actNewNotebook.setIcon(icon)
        self.actNewNotebook.setObjectName("actNewNotebook")
        self.actRecent = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open-recent")
        self.actRecent.setIcon(icon)
        self.actRecent.setObjectName("actRecent")
        self.actSaveAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.actSaveAll.setIcon(icon)
        self.actSaveAll.setObjectName("actSaveAll")
        self.actNoteNew = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actNoteNew.setIcon(icon)
        self.actNoteNew.setObjectName("actNoteNew")
        self.actNotePrevious = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.actNotePrevious.setIcon(icon)
        self.actNotePrevious.setObjectName("actNotePrevious")
        self.actNoteNext = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.actNoteNext.setIcon(icon)
        self.actNoteNext.setObjectName("actNoteNext")
        self.actNoteDelete = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actNoteDelete.setIcon(icon)
        self.actNoteDelete.setObjectName("actNoteDelete")
        self.actFilterPanel = QtWidgets.QAction(MainWindow)
        self.actFilterPanel.setCheckable(True)
        self.actFilterPanel.setObjectName("actFilterPanel")
        self.actToggleCalendar = QtWidgets.QAction(MainWindow)
        self.actToggleCalendar.setCheckable(True)
        icon = QtGui.QIcon.fromTheme("x-office-calendar")
        self.actToggleCalendar.setIcon(icon)
        self.actToggleCalendar.setObjectName("actToggleCalendar")
        self.actToggleTags = QtWidgets.QAction(MainWindow)
        self.actToggleTags.setCheckable(True)
        self.actToggleTags.setObjectName("actToggleTags")
        self.actToggleWords = QtWidgets.QAction(MainWindow)
        self.actToggleWords.setCheckable(True)
        self.actToggleWords.setObjectName("actToggleWords")
        self.actToggleList = QtWidgets.QAction(MainWindow)
        self.actToggleList.setCheckable(True)
        icon = QtGui.QIcon.fromTheme("view-sort-ascending")
        self.actToggleList.setIcon(icon)
        self.actToggleList.setObjectName("actToggleList")
        self.actNoteUp = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.actNoteUp.setIcon(icon)
        self.actNoteUp.setObjectName("actNoteUp")
        self.actNoteDown = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.actNoteDown.setIcon(icon)
        self.actNoteDown.setObjectName("actNoteDown")
        self.menu_File.addAction(self.actNewNotebook)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actOpenNotebook)
        self.menu_File.addAction(self.actRecent)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actSaveAll)
        self.menu_File.addAction(self.actCloseCurrent)
        self.menu_File.addAction(self.actQuit)
        self.menu_Edit.addAction(self.actionPreferences)
        self.menuNote.addAction(self.actNotePrevious)
        self.menuNote.addAction(self.actNoteNext)
        self.menuNote.addAction(self.actNoteUp)
        self.menuNote.addAction(self.actNoteDown)
        self.menuNote.addSeparator()
        self.menuNote.addAction(self.actNoteNew)
        self.menuNote.addAction(self.actNoteDelete)
        self.menuView.addAction(self.actFilterPanel)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actToggleCalendar)
        self.menuView.addAction(self.actToggleTags)
        self.menuView.addAction(self.actToggleWords)
        self.menuView.addAction(self.actToggleList)
        self.menuView.addSeparator()
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuNote.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actNewNotebook)
        self.toolBar.addAction(self.actCloseCurrent)
        self.toolBar.addAction(self.actRecent)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actNoteNew)
        self.toolBar.addAction(self.actNoteDelete)
        self.toolBar.addAction(self.actNotePrevious)
        self.toolBar.addAction(self.actNoteNext)

        self.retranslateUi(MainWindow)
        self.editor.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tblList.setSortingEnabled(True)
        self.noteDate.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.menuNote.setTitle(_translate("MainWindow", "Note"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actOpenNotebook.setText(_translate("MainWindow", "&Open Notebook"))
        self.actOpenNotebook.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionPreferences.setText(_translate("MainWindow", "&Preferences"))
        self.actQuit.setText(_translate("MainWindow", "&Quit"))
        self.actQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actCloseCurrent.setText(_translate("MainWindow", "&Closes notebook"))
        self.actCloseCurrent.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actNewNotebook.setText(_translate("MainWindow", "&New Notebook"))
        self.actRecent.setText(_translate("MainWindow", "&Recent Notebook"))
        self.actSaveAll.setText(_translate("MainWindow", "Save All Notebooks"))
        self.actSaveAll.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actNoteNew.setText(_translate("MainWindow", "New Note"))
        self.actNoteNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actNotePrevious.setText(_translate("MainWindow", "Previous"))
        self.actNotePrevious.setShortcut(_translate("MainWindow", "Ctrl+Left"))
        self.actNoteNext.setText(_translate("MainWindow", "Next"))
        self.actNoteNext.setShortcut(_translate("MainWindow", "Ctrl+Right"))
        self.actNoteDelete.setText(_translate("MainWindow", "Delete Note"))
        self.actNoteDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actFilterPanel.setText(_translate("MainWindow", "Filter panel"))
        self.actFilterPanel.setShortcut(_translate("MainWindow", "F3"))
        self.actToggleCalendar.setText(_translate("MainWindow", "Calendar"))
        self.actToggleTags.setText(_translate("MainWindow", "Tags Cloud"))
        self.actToggleWords.setText(_translate("MainWindow", "Words Cloud"))
        self.actToggleList.setText(_translate("MainWindow", "List"))
        self.actNoteUp.setText(_translate("MainWindow", "Up"))
        self.actNoteUp.setShortcut(_translate("MainWindow", "Ctrl+Up"))
        self.actNoteDown.setText(_translate("MainWindow", "Down"))
        self.actNoteDown.setShortcut(_translate("MainWindow", "Ctrl+Down"))

from flownote.ui.views.cloudView import cloudView
from PyQt5.QtWidgets import QTabBar
from flownote.ui.views.scrollView import scrollView
from flownote.ui.views.noteEdit import noteEdit
