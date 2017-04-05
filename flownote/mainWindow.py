#!/usr/bin/env python
# --!-- coding: utf8 --!--
import imp
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from flownote.ui.mainWindow_ui import Ui_MainWindow
from flownote.functions import *
from flownote.ui import style as S

from flownote.models.notebook import Notebook
from flownote.models.note import Note
from flownote.ui.dialogs.folderDialog import folderDialog
import flownote.functions as F


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
        self.txtNoteTitle.setStyleSheet(S.lineEditSS_2())
        self.txtDate.setStyleSheet("background:transparent;")
        #self.tab.setStyleSheet(S.tabBarSS())
        self.text.setStyleSheet(S.textEditorSS())
        self.tab.setShape(self.tab.RoundedWest)
        
        self.tblList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tblList.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblList.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Toggle filters
        self.actFilterPanel.toggled.connect(self.filter.setVisible)
        self.actToggleCalendar.toggled.connect(self.wdgCalendar.setVisible)
        self.actToggleTags.toggled.connect(self.lstTags.setVisible)
        self.actToggleWords.toggled.connect(self.lstWords.setVisible)
        self.actToggleList.toggled.connect(self.grpNotes.setVisible)
        
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
        self.cmbTheme = QComboBox()
        self.statusBar().addPermanentWidget(self.cmbTheme)
        themestr = open(F.appPath('flownote/themes/themes.json'),'r').read()
        self.themes = json.loads(themestr)
        self.themes["default"] = self.text.highlighter.defaultTheme
        self.cmbTheme.addItems(self.themes.keys())
        self.cmbTheme.currentIndexChanged[str].connect(self.changeTheme)
        
        # Hiding 
        self.actFilterPanel.setChecked(True)
        self.actToggleCalendar.setChecked(True)
        self.actToggleTags.setChecked(True)
        self.actToggleWords.setChecked(False)
        self.actToggleWords.toggled.emit(False)
        self.actToggleList.setChecked(True)
        
        # Connections
        self.txtFilter.textChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.setupFilters)
        #self.tab.currentChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.updateUI)
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
        self.actOpenNotebook.triggered.connect(self.openNotebookDialog)
        self.actCloseCurrent.triggered.connect(self.closeCurrentNotebook)
        self.actSaveAll.triggered.connect(self.save)
        self.dateA = None
        self.dateB = None
        self.actNoteUp.triggered.connect(self.navigateUp)
        self.actNoteDown.triggered.connect(self.navigateDown)
        self.actNotePrevious.triggered.connect(self.navigatePrevious)
        self.actNoteNext.triggered.connect(self.navigateNext)
        self.actNoteNew.triggered.connect(self.newNote)
        self.actNoteDelete.triggered.connect(self.deleteNote)
        self.actNoteDelete.setEnabled(False)
        
        # NOTEBOOKS AND NOTES
        self.notebooks = []
        self.notes = []  # filtered notes
        self.history = []  # history of openned notes
        self.historyPos = 0  
        
        # Bullshit notebooks
        self.bullshitNoteBook("My Bullshit Notebook", "my bullshit notebook")
        
        path = "/home/olivier/Dropbox/Documents/Travail/Geekeries/Python/PyCharmProjects/flownote/tests/Loren Ipsum/"
        self.openNotebook(path)
        #self.notebooks.append(self.bullshitNoteBook("My serious Notebook", "serious"))
        #self.notebooks.append(self.bullshitNoteBook("An other one", "AnOtHer"))
        
        #self.setupFilters()
        #self.filterNotes()
        
    def message(self, message, t=2000):        
        self.statusBar().showMessage(message, t)
        
    def updateUI(self):
        # Tab bar 
        activeNotebook = len(self.notebooks) > 1 and self.tab.currentIndex() == 0
        self.actNoteNew.setEnabled(not activeNotebook)
        self.actCloseCurrent.setEnabled(not activeNotebook)

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
        self.noteDate.dateChanged.disconnect()
        self.noteDate.setDate(F.strToDate(note.date))
        self.noteDate.setEnabled(True)
        self.noteDate.dateChanged.connect(note.setDate)
        
        # Title
        self.txtNoteTitle.disconnect()
        self.txtNoteTitle.setText(note.title)
        self.txtNoteTitle.setEnabled(True)
        self.txtNoteTitle.textChanged.connect(note.setTitle)
        
        self.text.setFocus()
        self.actNoteDelete.setEnabled(True)
        
    def closeNote(self):
        self.text.setNote(None)
        self.txtNoteTitle.setText("")
        self.txtNoteTitle.setEnabled(False)
        self.noteDate.setDate(QDate())
        self.noteDate.setEnabled(False)
        self.actNoteDelete.setEnabled(False)
        
    def tblSelectRow(self, UID, blockSignal=True):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.blockSignals(blockSignal)
        self.tblList.setCurrentItem(item)
        self.tblList.blockSignals(False)
        
    def tblChangeRow(self, UID):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.setCurrentItem(item)
        self.tblList.itemSelectionChanged.emit()
            
#==============================================================================
#   SMALL STUFF
#==============================================================================
    
    def currentNotebook(self):
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
            
    def changeTheme(self, theme):
        self.text.highlighter.setTheme(self.themes[theme])
        
        
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
        for nb in self.notebooks:
            if os.path.abspath(path) == os.path.abspath(nb.path):
                self.message("Notebook is already open.")
                return
        
        nb = Notebook(path=path)
        self.notebooks.append(nb)
        
        self.setupNotebook(nb)
        
    def setupNotebook(self, nb):
        # Signals
        nb.noteChanged.connect(self.updateSingleTblNote)
        nb.noteChanged.connect(self.updateCalendar)
        nb.tagsAndWordsChanged.connect(self.setupTagsAndWords)
        nb.noteAdded.connect(self.noteAdded)
        nb.noteRemoved.connect(self.noteRemoved)
        
        self.setupNotebooks()    
    
    def closeCurrentNotebook(self):
        if len(self.notebooks) == 1:
            self.notebooks = []
            
        else:
            nb = self.currentNotebook()
            if nb:
                self.notebooks.remove(nb)
            
        self.setupNotebooks()
        
#==============================GTK================================================
#   BULLSHIT (delete me)      
#==============================================================================
        
    def bullshitNoteBook(self, name="Bullshit", path="bullshit"):
        import random, string, lorem
        path = "/home/olivier/Dropbox/Documents/Travail/Geekeries/Python/PyCharmProjects/flownote/tests/{}".format(path)
        nb = Notebook(name, path, create=True)
        for i in range(2):
            n = Note(
                date="{}-{:02d}-{:02d}".format(
                    random.randint(2017, 2017),
                    random.randint(4, 4),
                    random.randint(1, 30)
                    ),
                text="#"+lorem.text(),
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
        while self.tab.count():         # Remove all tabs
            self.tab.removeTab(0)
        if len(self.notebooks) > 1:
            self.tab.addTab("All")
            #self.tab.show()
            self.wdgTab.show()
            for nb in self.notebooks:
                self.tab.addTab(nb.name)
                self.tab.setTabData(self.tab.count()-1, nb.UID)
        else:
            #self.tab.hide()
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
        self.lstWords.setWords(F.countDicts([n.words() for n in notes]))
        self.lstTags.setWords(F.countDicts([n.tags() for n in notes]))
        
    def addTblItem(self, note, y=None):
        f = qApp.font()
        f.setPointSize(f.pointSize() * .8)
        
        if y is None:
            y = self.tblList.rowCount()
            self.tblList.setRowCount(y+1)
        
        i = QTableWidgetItem(note.date)
        i.setData(Qt.UserRole, note.UID)
        i.setForeground(Qt.darkGray)
        i.setFont(f)
        self.tblList.setItem(y, 0, i)
        self.tblList.setItem(y, 1, QTableWidgetItem(note.title or note.text[:50]))
        self.tblList.setItem(y, 2, QTableWidgetItem(str(note.UID)))
        
    def setupTblNotes(self):
        self.tblList.clearContents()
        
        notes = self.allNotes()
        self.tblList.setRowCount(len(notes))
        y = 0
        self.tblList.setSortingEnabled(False)
        for n in notes:
            self.addTblItem(n, y)
            y += 1
        self.tblList.setSortingEnabled(True)
        self.tblList.sortItems(0)
        
    def noteAdded(self, UID):
        note = self.noteFromUID(UID)
        self.tblList.setSortingEnabled(False)
        self.addTblItem(note)
        self.tblList.setSortingEnabled(True)
        self.tblList.sortItems(0)
        self.updateCalendar()
        
    def noteRemoved(self, UID):
        self.closeNote()
        self.tblList.blockSignals(True)
        self.setupTblNotes()
        self.tblList.blockSignals(False)
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
            notes = [n for n in notes if self.txtFilter.text().lower() in n.text.lower()]
        
        # Tag filter
        sel = [i.text() for i in self.lstTags.selectedItems()]
        if sel:
            # AND
#            notes = [n for n in notes if len([s for s in sel if s in n.text.lower()]) == len(sel)]
            # OR
            notes = [n for n in notes if len([s for s in sel if s in n.text.lower()])]
            
        # Word filter
        sel = [i.text() for i in self.lstWords.selectedItems()]
        if sel:
            # AND
            notes = [n for n in notes if len([s for s in sel if s in n.text.lower()]) == len(sel)]
            # OR
#            notes = [n for n in notes if len([s for s in sel if s in n.text.lower()])]
        
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
        #self.editor.setCurrentIndex(1)
        #self.scroll.setNotes(self.notes)
        
        notes = self.notes
        self.lstWords.setVisibleWords(F.countDicts([n.words() for n in notes]))
        self.lstTags.setVisibleWords(F.countDicts([n.tags() for n in notes]))
        
    
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
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        
        allDates = []
        [allDates.extend(n.date for n in self.notebookNotes())]
        allDates = list(allDates)
    
        filterDates = list([n.date for n in self.notes])
        
        # Selected date range
        if self.dateB:
            d = self.dateA
            cf = QTextCharFormat()
            cf.setBackground(QColor("#FFFF00"))
            while d <= self.dateB:
                self.calendar.setDateTextFormat(d, cf)
                d = d.addDays(1)
        
        # Notes
        for d in allDates:
            qd = F.strToDate(d)
            if not qd: continue
            cf = QTextCharFormat()
            #cf.setFontWeight(QFont.Bold)
            cf.setBackground(QColor("#11000000"))
                
            # In current filter
            if d in filterDates:
                #cf.setBackground(QColor("#11000000"))
                cf.setFontWeight(QFont.Bold)
                
                if self.dateB and self.dateA <= qd <= self.dateB:
                    cf.setBackground(QColor("#77999900"))
                    
            self.calendar.setDateTextFormat(qd, cf)
        