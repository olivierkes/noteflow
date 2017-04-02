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
            self.lstNotebooks,
            self.lstTags,
            self.lstWords]:
                w.setStyleSheet("QListWidget{{{}}}".format(S.transparentSS()))
                
        self.setStyleSheet(S.mainWindowSS())
        
        self.txtFilter.setStyleSheet(S.lineEditSS_2())
        self.txtNoteName.setStyleSheet(S.lineEditSS_2())
        #self.tab.setStyleSheet(S.tabBarSS())
        #self.text.setStyleSheet(S.textEditorSS())
        
        self.tblList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tblList.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblList.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.btnToggleNotebooks.toggled.connect(self.grpNotebooks.setVisible)
        self.btnToggleFilter.toggled.connect(self.txtFilter.setVisible)
        self.btnToggleCalendar.toggled.connect(self.calendar.setVisible)
        self.btnToggleTags.toggled.connect(self.lstTags.setVisible)
        #self.btnToggleTags.toggled.connect(self.lineTags.setVisible)
        self.btnToggleWords.toggled.connect(self.lstWords.setVisible)
        
        self.txtFilter.textChanged.connect(self.filterNotes)
        self.lstNotebooks.itemSelectionChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.filterNotes)
        self.tab.currentChanged.connect(self.updateUI)
        self.lstTags.itemSelectionChanged.connect(self.filterNotes)
        self.lstWords.itemSelectionChanged.connect(self.filterNotes)
        self.tblList.itemSelectionChanged.connect(self.openNote)
        self.calendar.selectionChanged.connect(self.filterNotes)
        self.btnSave.clicked.connect(self.save)
        self.scroll.noteSelected.connect(self.tblSelectRow)
        #self.scroll.noteActivated.connect(lambda i:self.tblSelectRow(i, False))
        self.scroll.noteActivated.connect(self.tblChangeRow)
        self.tblList.hideColumn(2)
        self.tblList.setStyleSheet(S.tableSS())
        
        
        # Hiding 
        
        self.btnToggleNotebooks.setChecked(False)
        self.btnToggleCalendar.setChecked(False)
#        self.btnToggleFilter.setChecked(False)
        #self.btnToggleTags.setChecked(False)
        self.btnToggleWords.setChecked(False)
        
        # NOTEBOOKS

        self.notebooks = []
        
        # Bullshit notebooks
        self.notebooks.append(self.bullshitNoteBook("My Bullshit Notebook"))
        self.notebooks.append(self.bullshitNoteBook("My serious Notebook"))
        self.notebooks.append(self.bullshitNoteBook("An other one"))
        
        self.setupFilters()
        self.filterNotes()
        
    def message(self, message, t=2000):        
        self.statusBar().showMessage(message, t)
        
    def updateUI(self):
        # Tab bar 
        activeJournal = self.tab.isVisible() and self.tab.currentIndex() == 0
        self.btnNewNotebook.setEnabled(not activeJournal)
        
#==============================================================================
#   OPEN / SAVE
#==============================================================================
    
    def save(self):
        for nb in self.notebooks:
            nb.save()
    
#==============================GTK================================================
#   BULLSHIT (delete me)      
#==============================================================================
        
    def bullshitNoteBook(self, name="Bullshit"):
        import random, string, lorem
        nb = Notebook(name)
        for i in range(100):
            n = Note(
                date="{}-{:02d}-{:02d}".format(
                    random.randint(2016, 2017),
                    random.randint(1, 12),
                    random.randint(1, 30)
                    ),
                text="#"+lorem.text()
                )
            nb.addNote(n)
        return nb
    
#==============================================================================
#   FILTERING  
#==============================================================================
    
    def allNotes(self):
        "Return all notes, sorted by date"
        notes = []
        for nb in self.notebooks:
            nb.sortNotes()
            for n in nb.notes:
                notes.append(n)
        return notes
        
    def filterNotes(self):
        notes = []
        
        # Notebooks
        nb = self.notebooks
        ## Method with QListWidget
        #sel = [i.text() for i in self.lstNotebooks.selectedItems()]
        #nb = [nb for nb in self.notebooks if nb.name in sel or not sel]

        ## Method wit tabbar
        if self.tab.isVisible() and self.tab.currentIndex() > 0:  
            # means more than one notebook, and "All Notebooks" is not selected
            nb = [nb for nb in self.notebooks if nb.name == self.tab.tabText(self.tab.currentIndex())]
        
        notes = []
        [notes.extend(nb2.notes) for nb2 in nb]
        
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
        
        # Calendar
        #if self.calendar.isVisible():
            #d = self.calendar.selectedDate()
            #t = "{}-{}-{}".format(d.year(), d.month(), d.day())
            #notes = [n for n in notes if n.date == t]
        
        
        self.notes = notes
        self.message("{}/{} notes displayed.".format(
            len(notes),
            len(self.allNotes())))
        self.updateFiltersUI()
        
#==============================================================================
#   SETTING UP FILTERS
#==============================================================================

    def setupFilters(self):
        self.updateNotebooks()
        self.setupTblNotes()
        self.updateCalendar()
        
        notes = self.allNotes()
        self.lstWords.setWords(F.countDicts([n.words() for n in notes]))
        self.lstTags.setWords(F.countDicts([n.tags() for n in notes]))
        
    def updateNotebooks(self):
        self.lstNotebooks.clear()
        for nb in self.notebooks:
            self.lstNotebooks.addItem(nb.name)
        sh = self.lstNotebooks.maximumSize()
        h = self.lstNotebooks.sizeHintForRow(0) * self.lstNotebooks.count() + \
            2 * self.lstNotebooks.frameWidth()
        sh.setHeight(h)
        self.lstNotebooks.setMaximumSize(sh)
        
        # TabBar
        self.tab.setDocumentMode(True)
        while self.tab.count():         # Remove all tabs
            self.tab.removeTab(0)
        if len(self.notebooks) > 1:
            self.tab.addTab("All")
            self.tab.show()
            for nb in self.notebooks:
                self.tab.addTab(nb.name)
        else:
            self.tab.hide()
        
        
    def setupTblNotes(self):
        self.tblList.clearContents()
        
        notes = self.allNotes()
        self.tblList.setRowCount(len(notes))
        y = 0
        for n in notes:
            i = QTableWidgetItem(n.date)
            i.setData(Qt.UserRole, n.UID)
            self.tblList.setItem(y, 0, i)
            self.tblList.setItem(y, 1, QTableWidgetItem(n.text))
            #self.tblList.setItem(y, 2, QTableWidgetItem(str(n.wordCount())))
            y += 1
          
#==============================================================================
#   UPDATINGS FILTERS UI
#==============================================================================

    def updateFiltersUI(self):
        self.updateCalendar(self.notes)
        self.updateTblNotes()
        self.editor.setCurrentIndex(1)
        self.scroll.setNotes(self.notes)
        
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
            
    def updateCalendar(self, notes=None):
        # clear all
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        
        if notes is None:
            notes = self.allNotes()
        
        cf = QTextCharFormat()
        cf.setFontWeight(QFont.Bold)
        cf.setBackground(QColor("#11000000"))
        
        for n in notes:
            y, m, d = n.date.split("-")
            d = QDate(int(y), int(m), int(d))
            self.calendar.setDateTextFormat(d, cf)
    
    def openNote(self):
        item = self.tblList.currentItem()
        UID = self.tblList.item(item.row(), 0).data(Qt.UserRole)
        note = [n for n in self.notes if n.UID == UID][0]
        self.text.setText(note.text)
        self.editor.setCurrentIndex(0)
        
    def tblSelectRow(self, UID, blockSignal=True):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.blockSignals(blockSignal)
        self.tblList.setCurrentItem(item)
        self.tblList.blockSignals(False)
        
    def tblChangeRow(self, UID):
        item = F.findRowByUserData(self.tblList, UID)
        self.tblList.setCurrentItem(item)
        self.tblList.itemSelectionChanged.emit()
        
        
class MyQTextEdit(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        
        self.document().contentsChanged.connect(self.sizeChange)
        self.heightMin = 0
        self.heightMax = 65000
        self.sizeChange()

    def resizeEvent(self, e):
        QTextEdit.resizeEvent(self, e)
        self.sizeChange()

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)