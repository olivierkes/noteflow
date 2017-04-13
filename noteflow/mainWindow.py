#!/usr/bin/env python
# --!-- coding: utf8 --!--
import imp
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from noteflow.ui.mainWindow_ui import Ui_MainWindow
from noteflow.functions import *
from noteflow.ui import style as S

from noteflow.models.notebook import Notebook
from noteflow.models.note import Note
from noteflow.models.tag import TagCollector

from noteflow.ui.widgets.folderDialog import folderDialog
from noteflow.ui.widgets.labelDate import LabelDate
from noteflow.ui.widgets.labelTextStats import LabelTextStats
from noteflow.ui.widgets.preferences import Preferences

import noteflow.functions as F
import noteflow.markdownFunctions as MD

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

#==============================================================================
#       UI Stuff
#==============================================================================

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 12)

        for w in [
            self.lstTags,
            self.lstWords]:
                w.setStyleSheet("QListWidget{{{}}}".format(S.transparentSS()))

        self.setStyleSheet(S.mainWindowSS())

        self.txtFilter.setStyleSheet(S.lineEditSS_2())
        self.txtDate.setStyleSheet("background:transparent;")
        #self.tab.setStyleSheet(S.tabBarSS())
        self.text.setStyleSheet(S.textEditorSS())
        self.tab.setShape(self.tab.RoundedWest)

        self.tblList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tblList.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblList.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # Toggle filters
        self.actViewFilterPanel.toggled.connect(self.filter.setVisible)
        self.actToggleCalendar.toggled.connect(self.wdgCalendar.setVisible)
        self.actToggleTags.toggled.connect(self.lstTags.setVisible)
        self.actToggleWords.toggled.connect(self.lstWords.setVisible)
        self.actToggleList.toggled.connect(self.grpNotes.setVisible)
        self.actViewToolbar.toggled.connect(self.toolBar.setVisible)
        self.toolBar.visibilityChanged.connect(self.actViewToolbar.setChecked)

        ## Buttons widget in status bar...
        #w = QWidget()
        #l = QHBoxLayout(w)
        #l.setSpacing(0)
        #self.btnToggleCalendar = QToolButton()
        #self.btnToggleTags = QToolButton()
        #self.btnToggleWords = QToolButton()
        #self.btnToggleList = QToolButton()

        #for btn, act in [
            #(self.btnToggleCalendar, self.actToggleCalendar),
            #(self.btnToggleTags, self.actToggleTags),
            #(self.btnToggleWords, self.actToggleWords),
            #(self.btnToggleList, self.actToggleList),
            #]:
            #btn.setDefaultAction(act)
            #l.addWidget(btn)
        #self.statusBar().addWidget(w)
        ##w.setStyleSheet("QToolButton{border: 1px solid;}")
        self.lblStats = LabelTextStats()
        self.statusBar().addPermanentWidget(self.lblStats)
        self.text.statsChanged.connect(self.lblStats.setStats)
        self.lblNoteDate = LabelDate()
        self.statusBar().addPermanentWidget(self.lblNoteDate)
        self.lblNoteDate.hide()

        # Hiding
        self.actViewFilterPanel.setChecked(True)
        self.actViewToolbar.setChecked(True)
        self.actToggleCalendar.setChecked(True)
        self.actToggleTags.setChecked(True)
        self.actToggleWords.setChecked(True)
#        self.actToggleWords.toggled.emit(False)
        self.actToggleList.setChecked(True)

        # Connections
        self.txtFilter.textChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.setupFilters)
        #self.tab.currentChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.updateUI)
        self.tab.tabBarDoubleClicked.connect(self.changeNotebookName)
        self.lstTags.itemSelectionChanged.connect(self.filterNotes)
        self.lstWords.itemSelectionChanged.connect(self.filterNotes)
        self.tblList.itemSelectionChanged.connect(self.listNoteActivated)
        self.calendar.selectionChanged.connect(self.calendarChanged)
        self.btnDateClear.clicked.connect(self.calendarCleared)
        self.wdgDateInfos.hide()
        self.scroll.noteSelected.connect(self.tblSelectRow)
        #self.scroll.noteActivated.connect(lambda i:self.tblSelectRow(i, False))
        self.scroll.noteActivated.connect(self.tblChangeRow)
        self.tblList.hideColumn(2)
        self.tblList.setStyleSheet(S.tableSS())
        self.actNewNotebook.triggered.connect(self.newNotebook)
        self.actOpenNotebook.triggered.connect(self.openNotebookDialog)
        self.actCloseCurrent.triggered.connect(self.closeCurrentNotebook)
        self.actSaveAll.triggered.connect(self.save)
        self.dateA = None
        self.dateB = None
        self.actPreferences.triggered.connect(self.popupPreferences)
        self.actNoteUp.triggered.connect(self.navigateUp)
        self.actNoteDown.triggered.connect(self.navigateDown)
        self.actNotePrevious.triggered.connect(self.navigatePrevious)
        self.actNotePrevious.setEnabled(False)
        self.actNoteNext.triggered.connect(self.navigateNext)
        self.actNoteNext.setEnabled(False)
        self.actNoteNew.triggered.connect(self.newNote)
        self.actNoteDelete.triggered.connect(self.deleteNote)
        self.actNoteDelete.setEnabled(False)
        self.actNotePreview.triggered.connect(self.previewNote)
        self.actNotePreview.setEnabled(False)

        self.actFormatBold.triggered.connect(self.text.bold)
        self.actFormatItalic.triggered.connect(self.text.italic)
        self.actFormatStrike.triggered.connect(self.text.strike)
        self.actFormatVerbatim.triggered.connect(self.text.verbatim)
        self.actFormatComment.triggered.connect(self.text.comment)
        self.actFormatCommentLine.triggered.connect(self.text.commentLine)
        self.actFormatSuperScript.triggered.connect(self.text.superscript)
        self.actFormatSubScript.triggered.connect(self.text.subscript)

        self.actFormatClear.triggered.connect(self.text.clearFormat)
        self.actFormatHeaderSetext1.triggered.connect(lambda: self.text.titleSetext(1))
        self.actFormatHeaderSetext1.setShortcut("Ctrl+Alt+1")
        self.actFormatHeaderSetext2.triggered.connect(lambda: self.text.titleSetext(2))
        self.actFormatHeaderSetext2.setShortcut("Ctrl+Alt+2")
        self.actFormatHeaderATX1.triggered.connect(lambda: self.text.titleATX(1))
        self.actFormatHeaderATX2.triggered.connect(lambda: self.text.titleATX(2))
        self.actFormatHeaderATX3.triggered.connect(lambda: self.text.titleATX(3))
        self.actFormatHeaderATX4.triggered.connect(lambda: self.text.titleATX(4))
        self.actFormatHeaderATX5.triggered.connect(lambda: self.text.titleATX(5))
        self.actFormatHeaderATX6.triggered.connect(lambda: self.text.titleATX(6))

        # Add some status tips
        self.tab.setStatusTip("CTRL+Tab to cycle through open notebooks. (CTRL+Shift+Tab to cycle backward)")
        self.calendar.setStatusTip("Click on a date to filter that date. " +
                                   "Then Shift-click an other date to select a range.")

        # Shortcuts for tab navigation
        QShortcut("Ctrl+Tab", self).activated.connect(lambda:
            self.tab.setCurrentIndex((self.tab.currentIndex() + 1) % self.tab.count())
            if self.tab.isVisible() else None)
        QShortcut("Ctrl+Shift+Tab", self).activated.connect(lambda:
            self.tab.setCurrentIndex((self.tab.currentIndex() - 1) % self.tab.count())
            if self.tab.isVisible() else None)

        self.updateUIforNoteOpen(False)

        self.loadRecents()
        self.editor.setCurrentIndex(0)

        # PREVIEW
        settings = self.web.settings()
#        settings.setFontFamily(QtWebKit.QWebSettings.StandardFont, 'Times New Roman')
        settings.setFontSize(settings.DefaultFontSize, 13)

        # NOTEBOOKS AND NOTES
        self.notebooks = []
        self.notes = []  # filtered notes
        self.history = []  # history of openned notes
        self.historyPos = 0

        # CUSTOM TAGS & WORDS
        self.tags = TagCollector()
        self.tags.addTag("TODO", color="#00F", background="#FF0") # border="#00F"
        self.tags.addTag("ut", color="#F00")
        self.tags.addTag("doLorem", background="#0F0", border="#F0F")
        self.tags.addTag("TEMporA", border="#F00")
        self.tags.tagsChanged.connect(self.tagsChanged)
        
        self.minWordSize = 3
        self.hiddenWords = []
        self.preferences = Preferences(self)  # Dialog
        self.customTag = None  # Dialog
#        self.lstWords._minValue = 3

        self.lstTags.setCustomTags(self.tags)
        self.tblList.setCustomTags(self.tags)

        # Bullshit notebooks
        self.openPreviousNotebooks()
        
    def message(self, message, t=2000):
        self.statusBar().showMessage(message, t)

    def updateUI(self):
        # Tab bar
        activeNotebook = len(self.notebooks) > 1 and self.tab.currentIndex() == 0
        self.actNoteNew.setEnabled(not activeNotebook)
        self.actCloseCurrent.setEnabled(not activeNotebook)
        
        nb = self.currentNotebook()
        if nb:
            self.setWindowTitle("Noteflow — {}".format(nb.name))
        else:
            self.setWindowTitle("Noteflow")

#==============================================================================
#   SETTINGS
#==============================================================================

    def popupPreferences(self):
        self.preferences.tab.setCurrentIndex(0)
        self.preferences.loadValues()
        self.preferences.show()

#==============================================================================
#   NAVIGATION
#==============================================================================

    def navigateUp(self):
        self.navigateDown(delta=-1)

    def navigateDown(self, checked=False, delta=1):
        """We declare checked only because it's called from a signal that sends
        checked. The only important value is delta: +1 for down, -1 for up.
        """
        i = self.tblList.currentRow() + delta
        while self.tblList.isRowHidden(i):
            i += delta
        item = self.tblList.item(i, 0)
        if item:
            self.tblList.setCurrentItem(item)

    def navigatePrevious(self):
        if not self.actNotePrevious.isEnabled():
            return
        self.historyPos -= 1
        UID = self.history[self.historyPos]
        self.openNote(UID, noHistory=True)

    def navigateNext(self):
        if not self.actNoteNext.isEnabled():
            return
        self.historyPos += 1
        UID = self.history[self.historyPos]
        self.openNote(UID, noHistory=True)

    def listNoteActivated(self):
        item = self.tblList.currentItem()
        UID = self.tblList.item(item.row(), 0).data(Qt.UserRole)
        self.openNote(UID)

    def openNote(self, UID, noHistory=False):
        note = self.noteFromUID(UID)
        if self.text.note == note:
            return
        self.tblSelectRow(UID)
        self.calendar.blockSignals(True)
        self.calendar.setSelectedDate(F.strToDate(note.date))
        self.calendar.blockSignals(False)

        # History
        if not noHistory:
            self.history.append(UID)
            self.historyPos = len(self.history) -1

        self.actNoteNext.setEnabled(self.historyPos < len(self.history) -1)
        self.actNotePrevious.setEnabled(self.historyPos > 0)

        # Text
        self.text.setNote(note)
        self.editor.setCurrentIndex(0)

        # Date
        try:
            self.lblNoteDate.dateChanged.disconnect()
        except:
            pass
        self.lblNoteDate.setDate(F.strToDate(note.date))
        self.lblNoteDate.show()
        self.lblNoteDate.dateChanged.connect(note.setDate)

        self.text.setFocus()
        self.updateUIforNoteOpen(True)

    def previewNote(self, preview):
        if preview:
            self.web.setStyleSheet("QWebView{{background:{}; font-size:12px;}}".format(
                S.window))
            source = MD.render(self.text.note.toText())
            self.web.setHtml(source)
            self.editor.setCurrentIndex(1)
        else:
            self.editor.setCurrentIndex(0)

    def closeNote(self):
        self.text.setNote(None)
        self.lblNoteDate.setDate(QDate())
        self.lblNoteDate.hide()
        self.updateUIforNoteOpen(False)

    def tblSelectRow(self, UID, blockSignal=True):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.blockSignals(blockSignal)
        self.tblList.setCurrentItem(item)
        self.tblList.blockSignals(False)

    def tblChangeRow(self, UID):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.setCurrentItem(item)
        self.tblList.itemSelectionChanged.emit()

    def updateUIforNoteOpen(self, isOpen):
        self.actNoteDelete.setEnabled(isOpen)
        self.actNotePreview.setEnabled(isOpen)
        self.actFormatBold.setEnabled(isOpen)
        self.actFormatItalic.setEnabled(isOpen)
        self.actFormatStrike.setEnabled(isOpen)
        self.actFormatVerbatim.setEnabled(isOpen)
        self.actFormatComment.setEnabled(isOpen)
        self.actFormatCommentLine.setEnabled(isOpen)
        self.actFormatClear.setEnabled(isOpen)
        self.actFormatHeaderSetext1.setEnabled(isOpen)
        self.actFormatHeaderSetext2.setEnabled(isOpen)
        self.actFormatHeaderATX1.setEnabled(isOpen)
        self.actFormatHeaderATX2.setEnabled(isOpen)
        self.actFormatHeaderATX3.setEnabled(isOpen)
        self.actFormatHeaderATX4.setEnabled(isOpen)
        self.actFormatHeaderATX5.setEnabled(isOpen)
        self.actFormatHeaderATX6.setEnabled(isOpen)
        self.menuHeader.setEnabled(isOpen)

#==============================================================================
#   WORDS & TAGS
#==============================================================================

    def addToHiddenWords(self, word):
        word = word.lower()
        if not word in self.hiddenWords:
            self.hiddenWords.append(word)
            self.setupTagsAndWords()
            self.filterNotes()
            self.preferences.loadValues()

    def setMinWordSize(self, size):
        if size != self.minWordSize:
            self.minWordSize = size
            self.setupTagsAndWords()
            self.filterNotes()
            self.preferences.loadValues()

    def setHiddenWords(self, words):
        words = [w.lower() for w in words if w]
        if words != self.hiddenWords:
            self.hiddenWords = words
            self.setupTagsAndWords()
            self.filterNotes()
            self.preferences.loadValues()

    def tagsChanged(self):
        self.preferences.loadValues()

    def customizeTag(self, tag):
        if not self.tags.contains(tag):
            self.tags.addTag(tag)

        self.preferences.show()
        self.preferences.loadValues()
        self.preferences.tab.setCurrentIndex(1)
        self.preferences.setCurrentTag(tag)

#==============================================================================
#   SMALL STUFF
#==============================================================================

    def currentNotebook(self):
        if len(self.notebooks) == 1:
            return self.notebooks[0]

        nb = [nb for nb in self.notebooks if nb.UID == self.tab.tabData(self.tab.currentIndex())]
        if nb:
            return nb[0]

    def noteFromUID(self, UID):
        return [n for n in self.allNotes() if n.UID == UID][0]

    def newNote(self):
        nb = self.currentNotebook()
        d = (self.dateA if self.dateA else QDate.currentDate()).toString(Qt.ISODate)
        n = nb.newNote(date=d)
        self.openNote(n.UID)

    def deleteNote(self):
        if not self.text.note:
            self.actNoteDelete.setEnabled(False)
            return
        else:
            n = self.text.note
            n._notebook.removeNote(n)

#==============================================================================
#   OPEN / SAVE
#==============================================================================

    def save(self):
        for nb in self.notebooks:
            nb.save()

    def openNotebookDialog(self):
        #QFileDialog.getExistingDirectory(options=QFileDialog.DontUseNativeDialog)
        d = folderDialog()
        r = d.exec()
        if r:
            self.openNotebook(d.result)

    def openNotebook(self, path):
        # We check that the notebook is not open
        
        if not os.path.exists(path):
            print("Error: the given path does not exist.")
            print("       {}".format(path))
            return
        
        for nb in self.notebooks:
            if os.path.abspath(path) == os.path.abspath(nb.path):
                self.message("Notebook is already open.")
                return

        nb = Notebook(path=path)
        self.notebooks.append(nb)
        print("Notebook opened: {}".format(nb.name))
        self.setupNotebook(nb)

    def newNotebook(self):
        # First, we get a name
        name = self.getNotebookName()
        if not name:
            name = "A Notebook With No Name"

        # Then we get a path
        path = QFileDialog.getExistingDirectory(self, "Select an empty directory")
        if not path:
            # Was cancelled...
            QMessageBox.critical(self, "Notebook creation failed",
                                 "You didn't select a valid folder.\nI cannot create a notebook without a folder.")
            return

        if len(os.listdir(path)):
            # The directory is not empty
            QMessageBox.critical(self, "Notebook creation failed",
                                 "The folder you selected is not empty.\nPlease try again.")
            return

        nb = Notebook(name=name, path=path, create=True)
        self.notebooks.append(nb)
        self.setupNotebook(nb)

    def getNotebookName(self, name=""):
        name, ok = QInputDialog.getText(self, "Enter Notebook name", "You can always change the name later", text=name)
        return name

    def changeNotebookName(self, index):
        if index == 0:
            # The "All" tabl
            return
        nb = [nb for nb in self.notebooks if nb.UID == self.tab.tabData(index)][0]
        name = self.getNotebookName(nb.name)
        if name:
            nb.name = name
            self.tab.setTabText(index, name)

    def setupNotebook(self, nb):
        # Signals
        nb.noteChanged.connect(self.updateSingleTblNote)
        nb.dateChanged.connect(self.updateSingleTblNote)
        nb.dateChanged.connect(self.updateCalendar)
        nb.tagsAndWordsChanged.connect(self.setupTagsAndWords)
        nb.noteAdded.connect(self.noteAdded)
        nb.noteRemoved.connect(self.noteRemoved)
        self.addToRecentNotebooks(nb)

        self.setupNotebooks()

    def closeCurrentNotebook(self):
        nb = self.currentNotebook()
        if self.text.note in nb.notes:
            self.closeNote()
        if nb:
            self.notebooks.remove(nb)
        self.setupNotebooks()

    def addToRecentNotebooks(self, nb):

        if not nb.name or not nb.path:
            return

        recents = self.getRecents()

        if (nb.name, nb.path) in recents:
            return

        recents.append((nb.name, nb.path))

        val = "\n".join(["{}\n{}".format(name, path) for name, path in recents])
        s = F.settings()
        s.setValue("recentNotebooks", val)
        self.loadRecents()

    def getRecents(self):
        s = F.settings()
        r = s.value("recentNotebooks", "")
        recents = []
        if r:
            r = r.split("\n")
            while r:
                path = r.pop()
                name = r.pop()
                if os.path.exists(path):
                    recents.append((name, path))
        return recents

    def loadRecents(self):
        recents = self.getRecents()

        if recents:
            m = QMenu()
            for name, path in recents:
                a = m.addAction(name)
                a.setStatusTip(path)
                a.setData(path)
                a.triggered.connect(self.openRecentNotebook)

            self.actRecent.setMenu(m)
            self.actRecent.setEnabled(True)
        else:
            self.actRecent.setMenu(QMenu())
            self.actRecent.setEnabled(False)

    def openRecentNotebook(self):
        path = self.sender().data()
        self.openNotebook(path)
        
    def openPreviousNotebooks(self):
        if F.settings("OpenLast", Qt.Checked, int):
            last = F.settings("OpenLastNotebooks", "", str).split("\n")
            for path in last:
                if not path:
                    continue
                self.openNotebook(path)
        # We call that in case no notebooks were openend
        self.setupNotebooks()
            
    def closeEvent(self, event):
        # Save openned notebooks
        p = []
        for nb in self.notebooks:
            p.append(nb.path)
        F.settings().setValue("OpenLastNotebooks", "\n".join(p))
        
        QWidget.closeEvent(self, event)

#==============================GTK================================================
#   BULLSHIT (delete me)
#==============================================================================

    def bullshitNoteBook(self, name="Bullshit", path="bullshit"):
        import random, lorem
        path = F.appPath("tests/{}".format(path))
        nb = Notebook(name, path, create=True)
        for i in range(20):
            n = Note(
                date="{}-{:02d}-{:02d}".format(
                    random.randint(2017, 2017),
                    random.randint(4, 4),
                    random.randint(1, 30)
                    ),
                text=lorem.sentence() + " #"+lorem.text(),
                title=lorem.sentence()
                )
            nb.addNote(n)
        self.notebooks.append(nb)
        self.setupNotebook(nb)

#==============================================================================
#   SETTING UP FILTERS
#==============================================================================

    def setupNotebooks(self):
        # TabBar
        self.tab.setDocumentMode(True)
        self._shortcuts = []

        while self.tab.count():         # Remove all tabs
            self.tab.removeTab(0)

        # We only show the tabBar if there are more than 1 notebooks
        if len(self.notebooks) > 1:
            # One tab to rule them all
            self.tab.addTab("All")
            self.wdgTab.show()

            for nb in self.notebooks:
                i = self.tab.addTab(nb.name)
                self.tab.setTabData(i, nb.UID)

        else:
            self.wdgTab.hide()

        self.updateUI()
        self.setupTblNotes()
        self.setupFilters()

    def setupFilters(self):
        self.updateCalendar()
        self.setupTagsAndWords()

        self.filterNotes()

    def setupTagsAndWords(self):
        notes = self.notebookNotes()
        words = F.countDicts([n.words() for n in notes])

        words = {w:words[w] for w in words if not w.lower() in self.hiddenWords and
                                              len(w) >= self.minWordSize}
        tags = F.countDicts([n.tags() for n in notes])
        tags = {t:tags[t] for t in tags if not t.lower() in self.hiddenWords}

        self.lstWords.setWords(words)
        self.lstTags.setWords(tags)

    def setupTblNotes(self):
        notes = self.allNotes()
        self.tblList.blockSignals(True)
        self.tblList.setupNotes(notes)
        self.tblList.blockSignals(False)

    def noteAdded(self, UID):
        note = self.noteFromUID(UID)
        self.tblList.addNote(note)
        self.updateCalendar()

    def noteRemoved(self, UID):
        self.closeNote()
        self.setupTblNotes()
        self.setupFilters()

    def updateSingleTblNote(self, UID):
        dateItem = F.findRowByUserData(self.tblList, UID)
        titleItem = self.tblList.item(dateItem.row(), 1)
        note = F.findNoteByUID(self.notebooks, UID)
        dateItem.setText(note.date)
        titleItem.setText(note.title or note.text[:50])

#==============================================================================
#   FILTERING
#==============================================================================

    def listNotes(self, notebooks):
        "Return a list of the notes contain in the list notebooks."
        notes = []
        [notes.extend(nb.notes) for nb in notebooks]
        return notes

    def allNotes(self):
        "Return all notes, from all notebooks."
        return self.listNotes(self.notebooks)

    def notebookNotes(self):
        "Return all notes from the selected notebook(s)."

        if self.tab.isVisible() and self.tab.currentIndex() > 0:
            # means more than one notebook, and "All Notebooks" is not selected
            nb = [nb for nb in self.notebooks if nb.UID == self.tab.tabData(self.tab.currentIndex())]
            return self.listNotes(nb)
        else:
            return self.allNotes()

    def filterNotes(self):
        notes = []

        ## Notebooks
        notes = self.notebookNotes()

        # Text filter
        if self.txtFilter.text():
            notes = [n for n in notes if self.txtFilter.text().lower() in n.wholeText().lower()]

        # Tag filter
        sel = [i.text() for i in self.lstTags.selectedItems()]
        if sel:
            # AND
           notes = [n for n in notes if len([s for s in sel if s.lower() in n.text.lower()]) == len(sel)]
            # OR
            #notes = [n for n in notes if len([s for s in sel if s.lower() in n.text.lower()])]

        # Word filter
        sel = [i.text() for i in self.lstWords.selectedItems()]
        if sel:
            # AND
            notes = [n for n in notes if len([s for s in sel if s in n.text.lower()]) == len(sel)]
            # OR
            #notes = [n for n in notes if len([s for s in sel if s in n.text.lower()])]

        #Calendar
        if self.dateA and self.dateB:
            notes = [n for n in notes if self.dateA <= F.strToDate(n.date) <= self.dateB]
        elif self.dateA:
            notes = [n for n in notes if self.dateA == F.strToDate(n.date)]

        self.notes = notes
        self.message("{}/{} notes displayed.".format(
            len(notes),
            len(self.allNotes())))

        self.updateFiltersUI()

    def calendarChanged(self):
        ctrl = qApp.keyboardModifiers() & Qt.ControlModifier or \
            qApp.keyboardModifiers() & Qt.ShiftModifier
        if not ctrl:
            self.dateA = self.calendar.selectedDate()
            self.dateB = None
            self.txtDate.setText("Selected date: {}".format(
                self.dateA.toString(Qt.ISODate)))
        else:
            self.dateB = self.calendar.selectedDate()
            if self.dateA is None:
                self.dateA = QDate.currentDate()
            if self.dateB < self.dateA:
                self.dateA, self.dateB = self.dateB, self.dateA
            self.txtDate.setText("Date range: {} - {}".format(
                self.dateA.toString(Qt.ISODate),
                self.dateB.toString(Qt.ISODate)))
        self.wdgDateInfos.show()
        self.filterNotes()

    def calendarCleared(self):
        self.wdgDateInfos.hide()
        self.dateA = None
        self.dateB = None
        self.filterNotes()

#==============================================================================
#   UPDATINGS FILTERS UI
#==============================================================================

    def updateFiltersUI(self):
        self.updateCalendar()
        self.updateTblNotes()

        notes = self.notes
        self.lstWords.setVisibleWords(F.countDicts([n.words() for n in notes]))
        self.lstTags.setVisibleWords(F.countDicts([n.tags() for n in notes]))

        #if self.text.note is None:
        #    self.editor.setCurrentIndex(1)
        #    self.scroll.setNotes(self.notes)

        # TextEdit Highlight
        self.text.setHighlighted(
            words=[i.text() for i in self.lstWords.selectedItems()] + [self.txtFilter.text()],
            tags=[i.text() for i in self.lstTags.selectedItems()])

    def updateTblNotes(self):
        UIDs = [n.UID for n in self.notes]

        for i in range(self.tblList.rowCount()):
            UID = self.tblList.item(i, 0).data(Qt.UserRole)
            if UID in UIDs:
                self.tblList.showRow(i)
            else:
                self.tblList.hideRow(i)

    def updateCalendar(self):
        # clear all
        f = QTextCharFormat()
        c = QColor(S.window)
        f.setBackground(c)
        for i in range(Qt.Monday, Qt.Saturday):
            self.calendar.setWeekdayTextFormat(i, f)
        #f.setBackground(c.darker())
        f.setForeground(Qt.red)
        for i in range(Qt.Saturday, Qt.Sunday+1):
            self.calendar.setWeekdayTextFormat(i, f)

        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

        allDates = []
        [allDates.extend(n.date for n in self.notebookNotes())]
        allDates = list(allDates)

        filterDates = list([n.date for n in self.notes])

        dateColor = c.darker(110) # QColor("#22000000")
        selectedColor = QColor("#FFFF00")
        selectedDateColor = QColor("#77999900")

        # Selected date range
        if self.dateB:
            d = self.dateA
            cf = QTextCharFormat()
            cf.setBackground(selectedColor)
            while d <= self.dateB:
                self.calendar.setDateTextFormat(d, cf)
                d = d.addDays(1)

        # Notes
        for d in allDates:
            qd = F.strToDate(d)
            if not qd: continue
            cf = QTextCharFormat()
            #cf.setFontWeight(QFont.Bold)
            cf.setBackground(dateColor)
            #cf.setForeground(Qt.white)

            # In current filter
            if d in filterDates:
                #cf.setBackground(QColor("#11000000"))
                cf.setFontWeight(QFont.Bold)

                if self.dateB and self.dateA <= qd <= self.dateB:
                    cf.setBackground(selectedDateColor)

            self.calendar.setDateTextFormat(qd, cf)

