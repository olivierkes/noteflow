# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'noteflow/ui/mainWindow_ui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wdgTab = QtWidgets.QWidget(self.centralwidget)
        self.wdgTab.setObjectName("wdgTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.wdgTab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tab = QTabBar(self.wdgTab)
        self.tab.setObjectName("tab")
        self.verticalLayout_5.addWidget(self.tab)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.wdgTab)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.filter = QtWidgets.QWidget(self.splitter)
        self.filter.setObjectName("filter")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.filter)
        self.verticalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wdgCalendar = QtWidgets.QWidget(self.filter)
        self.wdgCalendar.setObjectName("wdgCalendar")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.wdgCalendar)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout_7.setSpacing(0)
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
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
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
        self.tblList = tableView(self.grpNotes)
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
        self.textPage = QtWidgets.QWidget()
        self.textPage.setObjectName("textPage")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.textPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = noteEdit(self.textPage)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.wdgSearch = QtWidgets.QWidget(self.textPage)
        self.wdgSearch.setObjectName("wdgSearch")
        self.gridLayout = QtWidgets.QGridLayout(self.wdgSearch)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.btnSearchPrevious = QtWidgets.QPushButton(self.wdgSearch)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.btnSearchPrevious.setIcon(icon)
        self.btnSearchPrevious.setObjectName("btnSearchPrevious")
        self.gridLayout.addWidget(self.btnSearchPrevious, 0, 4, 1, 1)
        self.txtSearch = QtWidgets.QLineEdit(self.wdgSearch)
        self.txtSearch.setObjectName("txtSearch")
        self.gridLayout.addWidget(self.txtSearch, 0, 2, 1, 1)
        self.btnSearchNext = QtWidgets.QPushButton(self.wdgSearch)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.btnSearchNext.setIcon(icon)
        self.btnSearchNext.setObjectName("btnSearchNext")
        self.gridLayout.addWidget(self.btnSearchNext, 0, 3, 1, 1)
        self.btnSearchClose = QtWidgets.QPushButton(self.wdgSearch)
        self.btnSearchClose.setText("")
        icon = QtGui.QIcon.fromTheme("window-close")
        self.btnSearchClose.setIcon(icon)
        self.btnSearchClose.setFlat(True)
        self.btnSearchClose.setObjectName("btnSearchClose")
        self.gridLayout.addWidget(self.btnSearchClose, 0, 0, 1, 1)
        self.wdgSearchOptions = QtWidgets.QWidget(self.wdgSearch)
        self.wdgSearchOptions.setObjectName("wdgSearchOptions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.wdgSearchOptions)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.chkSearchSelection = QtWidgets.QCheckBox(self.wdgSearchOptions)
        self.chkSearchSelection.setEnabled(False)
        self.chkSearchSelection.setObjectName("chkSearchSelection")
        self.gridLayout_3.addWidget(self.chkSearchSelection, 1, 3, 1, 1)
        self.cmbSearchMode = QtWidgets.QComboBox(self.wdgSearchOptions)
        self.cmbSearchMode.setFrame(False)
        self.cmbSearchMode.setObjectName("cmbSearchMode")
        self.cmbSearchMode.addItem("")
        self.cmbSearchMode.addItem("")
        self.gridLayout_3.addWidget(self.cmbSearchMode, 1, 1, 1, 1)
        self.chkSearchCase = QtWidgets.QCheckBox(self.wdgSearchOptions)
        self.chkSearchCase.setObjectName("chkSearchCase")
        self.gridLayout_3.addWidget(self.chkSearchCase, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.wdgSearchOptions)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.wdgSearchOptions)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 0, 1, 4)
        self.gridLayout.addWidget(self.wdgSearchOptions, 2, 1, 1, 4)
        self.wdgSearchReplace = QtWidgets.QWidget(self.wdgSearch)
        self.wdgSearchReplace.setObjectName("wdgSearchReplace")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.wdgSearchReplace)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnSearchReplace = QtWidgets.QPushButton(self.wdgSearchReplace)
        self.btnSearchReplace.setObjectName("btnSearchReplace")
        self.gridLayout_2.addWidget(self.btnSearchReplace, 1, 4, 1, 1)
        self.txtSearchReplace = QtWidgets.QLineEdit(self.wdgSearchReplace)
        self.txtSearchReplace.setObjectName("txtSearchReplace")
        self.gridLayout_2.addWidget(self.txtSearchReplace, 1, 2, 1, 1)
        self.btnSearchReplaceAll = QtWidgets.QPushButton(self.wdgSearchReplace)
        self.btnSearchReplaceAll.setObjectName("btnSearchReplaceAll")
        self.gridLayout_2.addWidget(self.btnSearchReplaceAll, 1, 5, 1, 1)
        self.btnSearchOptions = QtWidgets.QPushButton(self.wdgSearchReplace)
        self.btnSearchOptions.setText("")
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnSearchOptions.setIcon(icon)
        self.btnSearchOptions.setCheckable(True)
        self.btnSearchOptions.setFlat(True)
        self.btnSearchOptions.setObjectName("btnSearchOptions")
        self.gridLayout_2.addWidget(self.btnSearchOptions, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.wdgSearchReplace, 1, 0, 1, 5)
        self.verticalLayout.addWidget(self.wdgSearch)
        self.editor.addWidget(self.textPage)
        self.previewPage = QtWidgets.QWidget()
        self.previewPage.setObjectName("previewPage")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.previewPage)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.editor.addWidget(self.previewPage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.html = QtWidgets.QTextBrowser(self.page)
        self.html.setObjectName("html")
        self.verticalLayout_9.addWidget(self.html)
        self.editor.addWidget(self.page)
        self.scrollPage = QtWidgets.QWidget()
        self.scrollPage.setObjectName("scrollPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollPage)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scroll = scrollView(self.scrollPage)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_6.addWidget(self.scroll)
        self.editor.addWidget(self.scrollPage)
        self.structure = structureView(self.splitter)
        self.structure.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.structure.setObjectName("structure")
        self.structure.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 30))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuNote = QtWidgets.QMenu(self.menubar)
        self.menuNote.setObjectName("menuNote")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFormat = QtWidgets.QMenu(self.menubar)
        self.menuFormat.setObjectName("menuFormat")
        self.menuHeader = QtWidgets.QMenu(self.menuFormat)
        self.menuHeader.setObjectName("menuHeader")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actOpenNotebook = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actOpenNotebook.setIcon(icon)
        self.actOpenNotebook.setObjectName("actOpenNotebook")
        self.actPreferences = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("preferences-system")
        self.actPreferences.setIcon(icon)
        self.actPreferences.setObjectName("actPreferences")
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
        self.actViewFilterPanel = QtWidgets.QAction(MainWindow)
        self.actViewFilterPanel.setCheckable(True)
        self.actViewFilterPanel.setObjectName("actViewFilterPanel")
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
        self.actThemes = QtWidgets.QAction(MainWindow)
        self.actThemes.setObjectName("actThemes")
        self.actViewToolbar = QtWidgets.QAction(MainWindow)
        self.actViewToolbar.setCheckable(True)
        self.actViewToolbar.setObjectName("actViewToolbar")
        self.actNotePreview = QtWidgets.QAction(MainWindow)
        self.actNotePreview.setCheckable(True)
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.actNotePreview.setIcon(icon)
        self.actNotePreview.setObjectName("actNotePreview")
        self.actFormatBold = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("format-text-bold")
        self.actFormatBold.setIcon(icon)
        self.actFormatBold.setObjectName("actFormatBold")
        self.actFormatItalic = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("format-text-italic")
        self.actFormatItalic.setIcon(icon)
        self.actFormatItalic.setObjectName("actFormatItalic")
        self.actFormatStrike = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("format-text-strikethrough")
        self.actFormatStrike.setIcon(icon)
        self.actFormatStrike.setObjectName("actFormatStrike")
        self.actFormatVerbatim = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("text-x-script")
        self.actFormatVerbatim.setIcon(icon)
        self.actFormatVerbatim.setObjectName("actFormatVerbatim")
        self.actFormatComment = QtWidgets.QAction(MainWindow)
        self.actFormatComment.setObjectName("actFormatComment")
        self.actFormatCommentLine = QtWidgets.QAction(MainWindow)
        self.actFormatCommentLine.setObjectName("actFormatCommentLine")
        self.actFormatClear = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.actFormatClear.setIcon(icon)
        self.actFormatClear.setObjectName("actFormatClear")
        self.actFormatHeaderSetext1 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderSetext1.setObjectName("actFormatHeaderSetext1")
        self.actFormatHeaderSetext2 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderSetext2.setObjectName("actFormatHeaderSetext2")
        self.actFormatHeaderATX1 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX1.setObjectName("actFormatHeaderATX1")
        self.actFormatHeaderATX2 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX2.setObjectName("actFormatHeaderATX2")
        self.actFormatHeaderATX3 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX3.setObjectName("actFormatHeaderATX3")
        self.actFormatHeaderATX4 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX4.setObjectName("actFormatHeaderATX4")
        self.actFormatHeaderATX5 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX5.setObjectName("actFormatHeaderATX5")
        self.actFormatHeaderATX6 = QtWidgets.QAction(MainWindow)
        self.actFormatHeaderATX6.setObjectName("actFormatHeaderATX6")
        self.actFormatSuperScript = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("format-text-superscript")
        self.actFormatSuperScript.setIcon(icon)
        self.actFormatSuperScript.setObjectName("actFormatSuperScript")
        self.actFormatSubScript = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("format-text-subscript")
        self.actFormatSubScript.setIcon(icon)
        self.actFormatSubScript.setObjectName("actFormatSubScript")
        self.actNoteSearch = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-find")
        self.actNoteSearch.setIcon(icon)
        self.actNoteSearch.setObjectName("actNoteSearch")
        self.actNoteReplace = QtWidgets.QAction(MainWindow)
        self.actNoteReplace.setObjectName("actNoteReplace")
        self.actViewStructure = QtWidgets.QAction(MainWindow)
        self.actViewStructure.setCheckable(True)
        self.actViewStructure.setObjectName("actViewStructure")
        self.menu_File.addAction(self.actNewNotebook)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actOpenNotebook)
        self.menu_File.addAction(self.actRecent)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actSaveAll)
        self.menu_File.addAction(self.actCloseCurrent)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actPreferences)
        self.menu_File.addAction(self.actQuit)
        self.menuNote.addAction(self.actNotePrevious)
        self.menuNote.addAction(self.actNoteNext)
        self.menuNote.addAction(self.actNoteUp)
        self.menuNote.addAction(self.actNoteDown)
        self.menuNote.addSeparator()
        self.menuNote.addAction(self.actNoteNew)
        self.menuNote.addAction(self.actNoteDelete)
        self.menuNote.addSeparator()
        self.menuNote.addAction(self.actNotePreview)
        self.menuNote.addAction(self.actNoteSearch)
        self.menuNote.addAction(self.actNoteReplace)
        self.menuView.addAction(self.actViewToolbar)
        self.menuView.addAction(self.actViewFilterPanel)
        self.menuView.addAction(self.actViewStructure)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actToggleCalendar)
        self.menuView.addAction(self.actToggleTags)
        self.menuView.addAction(self.actToggleWords)
        self.menuView.addAction(self.actToggleList)
        self.menuView.addSeparator()
        self.menuHeader.addAction(self.actFormatHeaderSetext1)
        self.menuHeader.addAction(self.actFormatHeaderSetext2)
        self.menuHeader.addSeparator()
        self.menuHeader.addAction(self.actFormatHeaderATX1)
        self.menuHeader.addAction(self.actFormatHeaderATX2)
        self.menuHeader.addAction(self.actFormatHeaderATX3)
        self.menuHeader.addAction(self.actFormatHeaderATX4)
        self.menuHeader.addAction(self.actFormatHeaderATX5)
        self.menuHeader.addAction(self.actFormatHeaderATX6)
        self.menuFormat.addAction(self.menuHeader.menuAction())
        self.menuFormat.addSeparator()
        self.menuFormat.addAction(self.actFormatBold)
        self.menuFormat.addAction(self.actFormatItalic)
        self.menuFormat.addAction(self.actFormatStrike)
        self.menuFormat.addAction(self.actFormatVerbatim)
        self.menuFormat.addAction(self.actFormatSuperScript)
        self.menuFormat.addAction(self.actFormatSubScript)
        self.menuFormat.addAction(self.actFormatComment)
        self.menuFormat.addAction(self.actFormatCommentLine)
        self.menuFormat.addSeparator()
        self.menuFormat.addAction(self.actFormatClear)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuNote.menuAction())
        self.menubar.addAction(self.menuFormat.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actNewNotebook)
        self.toolBar.addAction(self.actOpenNotebook)
        self.toolBar.addAction(self.actSaveAll)
        self.toolBar.addAction(self.actCloseCurrent)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actPreferences)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actNoteNew)
        self.toolBar.addAction(self.actNoteDelete)
        self.toolBar.addAction(self.actNotePreview)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actNotePrevious)
        self.toolBar.addAction(self.actNoteNext)

        self.retranslateUi(MainWindow)
        self.editor.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.txtDate, self.btnDateClear)
        MainWindow.setTabOrder(self.btnDateClear, self.lstTags)
        MainWindow.setTabOrder(self.lstTags, self.lstWords)
        MainWindow.setTabOrder(self.lstWords, self.txtFilter)
        MainWindow.setTabOrder(self.txtFilter, self.tblList)
        MainWindow.setTabOrder(self.tblList, self.text)
        MainWindow.setTabOrder(self.text, self.scroll)
        MainWindow.setTabOrder(self.scroll, self.txtSearch)
        MainWindow.setTabOrder(self.txtSearch, self.txtSearchReplace)
        MainWindow.setTabOrder(self.txtSearchReplace, self.btnSearchNext)
        MainWindow.setTabOrder(self.btnSearchNext, self.btnSearchPrevious)
        MainWindow.setTabOrder(self.btnSearchPrevious, self.btnSearchReplace)
        MainWindow.setTabOrder(self.btnSearchReplace, self.btnSearchReplaceAll)
        MainWindow.setTabOrder(self.btnSearchReplaceAll, self.cmbSearchMode)
        MainWindow.setTabOrder(self.cmbSearchMode, self.chkSearchCase)
        MainWindow.setTabOrder(self.chkSearchCase, self.chkSearchSelection)
        MainWindow.setTabOrder(self.chkSearchSelection, self.calendar)
        MainWindow.setTabOrder(self.calendar, self.html)
        MainWindow.setTabOrder(self.html, self.btnSearchClose)
        MainWindow.setTabOrder(self.btnSearchClose, self.btnSearchOptions)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Noteflow"))
        self.txtDate.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">Search bar</span></p><p><br/></p><p><span style=\" font-weight:600;\">Multi-words search:</span> separate with space.</p><p><span style=\" font-style:italic;\">Ex: word1 word2 word3</span></p><p><br/></p><p><span style=\" font-weight:600;\">Phrase searh:</span> wrap in double quotes</p><p><span style=\" font-style:italic;\">Ex: word1 &quot;word2 word3&quot;</span></p><p><br/></p><p><span style=\" font-weight:600;\">Filters:</span></p><p>* &quot;t:word&quot; searches for &quot;word&quot; in note title</p><p>* &quot;#:word&quot; filters hashtags cloud for tags matching &quot;word&quot;</p></body></html>"))
        self.tblList.setSortingEnabled(True)
        self.btnSearchPrevious.setText(_translate("MainWindow", "Previous"))
        self.txtSearch.setPlaceholderText(_translate("MainWindow", "Search"))
        self.btnSearchNext.setText(_translate("MainWindow", "Next"))
        self.chkSearchSelection.setText(_translate("MainWindow", "Selection only"))
        self.cmbSearchMode.setItemText(0, _translate("MainWindow", "Plain text"))
        self.cmbSearchMode.setItemText(1, _translate("MainWindow", "RegExp"))
        self.chkSearchCase.setText(_translate("MainWindow", "Match case"))
        self.label_3.setText(_translate("MainWindow", "Mode:"))
        self.btnSearchReplace.setText(_translate("MainWindow", "Replace"))
        self.txtSearchReplace.setPlaceholderText(_translate("MainWindow", "Replace"))
        self.btnSearchReplaceAll.setText(_translate("MainWindow", "Replace all"))
        self.menu_File.setTitle(_translate("MainWindow", "&Notebook"))
        self.menuNote.setTitle(_translate("MainWindow", "Note"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuFormat.setTitle(_translate("MainWindow", "&Format"))
        self.menuHeader.setTitle(_translate("MainWindow", "Header"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actOpenNotebook.setText(_translate("MainWindow", "&Open"))
        self.actOpenNotebook.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actPreferences.setText(_translate("MainWindow", "&Preferences"))
        self.actPreferences.setShortcut(_translate("MainWindow", "Ctrl+F8"))
        self.actQuit.setText(_translate("MainWindow", "&Quit"))
        self.actQuit.setShortcut(_translate("MainWindow", "Alt+F4"))
        self.actCloseCurrent.setText(_translate("MainWindow", "&Close notebook"))
        self.actCloseCurrent.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actNewNotebook.setText(_translate("MainWindow", "&New Notebook"))
        self.actNewNotebook.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actRecent.setText(_translate("MainWindow", "&Recent"))
        self.actSaveAll.setText(_translate("MainWindow", "Save All"))
        self.actSaveAll.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actNoteNew.setText(_translate("MainWindow", "New Note"))
        self.actNoteNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actNotePrevious.setText(_translate("MainWindow", "Previous"))
        self.actNotePrevious.setShortcut(_translate("MainWindow", "Alt+Left"))
        self.actNoteNext.setText(_translate("MainWindow", "Next"))
        self.actNoteNext.setShortcut(_translate("MainWindow", "Alt+Right"))
        self.actNoteDelete.setText(_translate("MainWindow", "Delete Note"))
        self.actNoteDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actViewFilterPanel.setText(_translate("MainWindow", "Filter panel"))
        self.actViewFilterPanel.setShortcut(_translate("MainWindow", "F2"))
        self.actToggleCalendar.setText(_translate("MainWindow", "Calendar"))
        self.actToggleTags.setText(_translate("MainWindow", "Tags Cloud"))
        self.actToggleWords.setText(_translate("MainWindow", "Words Cloud"))
        self.actToggleList.setText(_translate("MainWindow", "List"))
        self.actNoteUp.setText(_translate("MainWindow", "Up"))
        self.actNoteUp.setShortcut(_translate("MainWindow", "Alt+Up"))
        self.actNoteDown.setText(_translate("MainWindow", "Down"))
        self.actNoteDown.setShortcut(_translate("MainWindow", "Alt+Down"))
        self.actThemes.setText(_translate("MainWindow", "Themes"))
        self.actViewToolbar.setText(_translate("MainWindow", "Toolbar"))
        self.actNotePreview.setText(_translate("MainWindow", "Preview"))
        self.actNotePreview.setShortcut(_translate("MainWindow", "F3"))
        self.actFormatBold.setText(_translate("MainWindow", "Bold"))
        self.actFormatBold.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actFormatItalic.setText(_translate("MainWindow", "Italic"))
        self.actFormatItalic.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actFormatStrike.setText(_translate("MainWindow", "Strike"))
        self.actFormatVerbatim.setText(_translate("MainWindow", "Verbatim"))
        self.actFormatComment.setText(_translate("MainWindow", "Comment"))
        self.actFormatComment.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.actFormatCommentLine.setText(_translate("MainWindow", "Comment Line"))
        self.actFormatCommentLine.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actFormatClear.setText(_translate("MainWindow", "Clear"))
        self.actFormatClear.setShortcut(_translate("MainWindow", "Ctrl+0"))
        self.actFormatHeaderSetext1.setText(_translate("MainWindow", "Level 1 (Setext)"))
        self.actFormatHeaderSetext2.setText(_translate("MainWindow", "Level 2 (Setext)"))
        self.actFormatHeaderATX1.setText(_translate("MainWindow", "Level 1 (atx)"))
        self.actFormatHeaderATX1.setToolTip(_translate("MainWindow", "Level 1 (ATX)"))
        self.actFormatHeaderATX1.setShortcut(_translate("MainWindow", "Ctrl+1"))
        self.actFormatHeaderATX2.setText(_translate("MainWindow", "Level 2"))
        self.actFormatHeaderATX2.setShortcut(_translate("MainWindow", "Ctrl+2"))
        self.actFormatHeaderATX3.setText(_translate("MainWindow", "Level 3"))
        self.actFormatHeaderATX3.setShortcut(_translate("MainWindow", "Ctrl+3"))
        self.actFormatHeaderATX4.setText(_translate("MainWindow", "Level 4"))
        self.actFormatHeaderATX4.setShortcut(_translate("MainWindow", "Ctrl+4"))
        self.actFormatHeaderATX5.setText(_translate("MainWindow", "Level 5"))
        self.actFormatHeaderATX5.setShortcut(_translate("MainWindow", "Ctrl+5"))
        self.actFormatHeaderATX6.setText(_translate("MainWindow", "Level 6"))
        self.actFormatHeaderATX6.setShortcut(_translate("MainWindow", "Ctrl+6"))
        self.actFormatSuperScript.setText(_translate("MainWindow", "Superscript"))
        self.actFormatSuperScript.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.actFormatSubScript.setText(_translate("MainWindow", "Subscript"))
        self.actFormatSubScript.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.actNoteSearch.setText(_translate("MainWindow", "&Find…"))
        self.actNoteSearch.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actNoteReplace.setText(_translate("MainWindow", "&Replace…"))
        self.actNoteReplace.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actViewStructure.setText(_translate("MainWindow", "Structure"))
        self.actViewStructure.setShortcut(_translate("MainWindow", "F4"))

from PyQt5.QtWidgets import QTabBar
from noteflow.ui.views.cloudView import cloudView
from noteflow.ui.views.noteEdit import noteEdit
from noteflow.ui.views.scrollView import scrollView
from noteflow.ui.views.structureView import structureView
from noteflow.ui.views.tableView import tableView
