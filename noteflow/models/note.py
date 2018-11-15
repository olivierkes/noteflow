#!/usr/bin/env python
# --!-- coding: utf8 --!--

import re

import noteflow.functions as F
from PyQt5.QtCore import *

class Note(QObject):

    tagsAndWordsChanged = pyqtSignal(int)
    #metaChanged = pyqtSignal()  # Emited when date or title changes
    dateChanged = pyqtSignal(int)  # When the date changes. Param is UID
    noteChanged = pyqtSignal(int)  # When anything else changes. Param is UID

    def __init__(self, date=None, text="", title="", fromText=""):
        QObject.__init__(self)
        if not fromText:
            # We are creating a new note
            self.date = date
            self.text = text
            self.title = title

        if fromText:
            # Creating from a disk file
            self.fromText(fromText)

        self.UID = F.uniqueID()
        self._words = None
        self._tags = None
        self._filename = None

        # Temp var, not saved
        self._posInNoteScroll = 0  # Used by noteEdit to remember the ratio of the vertical scrollbar
        self._posInNoteCursor = 0 # Position of the cursor

    def tags(self):
        "Returns all tags within the note."
        if not self._tags:
            self._tags = self.generateTags()

        return self._tags

    def generateTags(self):
        tags = re.compile('#[\w]+').findall(self.text)
        tags = [t.lower() for t in tags if t[0] == "#"]
        return F.countWords(tags)

    def words(self):
        "Returns all words within the note."
        if not self._words:
            self._words = self.generateWords()

        return self._words

    def wordCount(self):
        return len(re.compile('\w+').findall(self.text))

    def generateWords(self):
        "Returns a dict of words with the number of time they appear in the note."
        words = re.compile('[\w]+').findall(self.text)
        words = [w.lower() for w in words]

        return F.countWords(words)

    def setDate(self, date):
        d = date.toString(Qt.ISODate)
        if self._notebook and d != self.date:
            self.date = d
            self.dateChanged.emit(self.UID)

    def setWholeText(self, text):
        if self._notebook:
            title, text = self.splitWholeText(text)
            if text != self.text:
                self.setText(text)
            if title != self.title:
                self.setTitle(title)

    def wholeText(self):
        return "{}\n{}".format(
            self.title,
            self.text)

    def setText(self, text):
        if self._notebook and text != self.text:
            self.text = text
            self.noteChanged.emit(self.UID)
            t = self.generateTags()
            w = self.generateWords()
            if t != self._tags or w != self._words:
                self._tags = t
                self._words = w
                self.tagsAndWordsChanged.emit(self.UID)

    def splitWholeText(self, text):
        txt = text.split("\n")
        title = txt[0]
        text = "\n".join(txt[1:]) if len(txt) > 1 else ""
        return title, text

    def setTitle(self, title):
        if self._notebook and title != self.title:
            self.title = title
            self.noteChanged.emit(self.UID)

#==============================================================================
#   LOAD / SAVE
#==============================================================================

    def toText(self):

        # If note is empty (except for date, since it must have one), we don't save.
        if not self.title and not self.text:
            return ""

        # Metadata, pandoc_title_block style
        t = "% {title}\n% {author}\n% {date}\n\n{content}".format(
            title=self.title,
            author="",
            date=self.date,
            content=self.text)
        return t

    def fromText(self, text):
        lines = text.split("\n")
        self.title = lines[0][2:]
        self.date = lines[2][2:]
        self.text = "\n".join(lines[4:])
