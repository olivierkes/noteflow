#!/usr/bin/env python
# --!-- coding: utf8 --!--

import json, os, re
import noteflow.functions as F
from noteflow.models.note import Note
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

EXT = ".txt"

class Notebook(QObject):
    """A collection of notes.

    On the computer, a notebook is a folder containing text files.
    """

    noteChanged = pyqtSignal(int)  # param int is the note UID
    dateChanged = pyqtSignal(int)  # param int is the note UID
    tagsAndWordsChanged = pyqtSignal(int)  # param int is the note UID
    noteAdded = pyqtSignal(int)
    noteRemoved = pyqtSignal(int)

    def __init__(self, name=None, path=None, create=False, MW=None):
        QObject.__init__(self)
        self.notes = []
        self._cmdTimers = []

        if create:
            assert(name)
            assert(path)
            self.name = name
            self.path = path
            self._content = {}

        else:
            # We must load from path
            ini = os.path.join(path, ".NOTEFLOW")
            assert os.path.exists(ini)
            s = QSettings(ini, QSettings.IniFormat)
            self.name = s.value("Name")
            self.path = path

            # Read Settings
            tags = s.value("Tags")
            if tags and MW:
                for t in tags.split("\n"):
                    n, c1, c2, c3 = t.split(",")
                    if not MW.tags.find(n):
                        MW.tags.addTag(
                            n,
                            color=c1 if c1 else None,
                            background=c2 if c2 else None,
                            border=c3 if c3 else None)
            hidden = s.value("Exclude")
            if hidden and MW:
                for w in hidden.split(","):
                    if not w.strip() in MW.hiddenWords:
                        MW.hiddenWords.append(w)

            self.load(path)

        self.UID = F.uniqueID()

    def newNote(self, date=None, text="", title=""):
        n = Note(date=date, text=text, title=title)
        self.addNote(n)
        self.noteAdded.emit(n.UID)
        return n

    def addNote(self, note):
        self.notes.append(note)
        note._notebook = self
        note.noteChanged.connect(self.noteChanged)
        note.dateChanged.connect(self.dateChanged)
        note.tagsAndWordsChanged.connect(self.tagsAndWordsChanged)

    def removeNote(self, note):
        self.notes.remove(note)
        note._notebook = None
        UID = note.UID
        note = None
        self.noteRemoved.emit(UID)

    def sortNotes(self):
        "Internally sort notes by dates."
        self.notes = self.sorted(self.notes)

    def sorted(self, notes):
        return sorted(notes, key=lambda n: n.date)

#==============================================================================
#   LOAD / SAVE
#==============================================================================

    def notesToDisk(self):
        files = {}
        for n in self.notes:
            path = "{y}/{m}/{date}{title}".format(
                y=n.date.split("-")[0],
                m=n.date.split("-")[1],
                date=n.date,
                title="-"+F.slugify(n.title) if n.title else "")
            content = n.toText()

            if not content:
                # We don't save empty notes
                continue

            # Make sure no two files have the same path
            n = 2
            nPath = path
            while nPath+EXT in files:
                nPath = "{}_{}".format(path, n)
                n += 1
            path = nPath+EXT

            files[path] = content
        return files


    def load(self, path):
        # Read content
        content = {}
        for root, dirs, files in os.walk(path):
            for f in files:
                if f[-len(EXT):] == EXT:
                    filename = os.path.join(root, f)
                    p = os.path.relpath(filename, path)
                    content[p] = F.loadTextFile(filename)

        self._content = content

        # Add content as note
        for p in content:
            self.addNote(Note(fromText=content[p]))

    def save(self):
        print("Saving in: {}".format(self.path))

        content = self.notesToDisk()
        oldContent = self._content
        changed = 0

        # Writing content
        for path in content:

            filename = os.path.join(self.path, path)
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            if path in oldContent and content[path] == oldContent[path]:
                # Nothing to do, file didn't change
                pass

            else:
                # The content of the file changed, or the file is new. We write.
                print("Writing:", path)
                changed += 1
                with open(filename, "w", encoding='utf8') as f:
                    f.write(content[path])

                # MACRO COMMANDS
                #---------------

                # STORE VARS
                vars = {}
                for m in re.finditer(r'@noteflow:\s*var\s*([^\s]+)\s*=\s*("(.+)"|[^\s]+)',
                                     content[path], re.I):
                    value = m.group(2).strip()
                    if value[0] == value[-1] == '"':
                         value = value[1:-1]
                    print("VAR {name} = {value}".format(
                        name=m.group(1).strip(),
                        value=value))
                    vars[m.group(1)] = value

                # EXPORT TO EXTRA LOCATION
                # Searches for something like `@noteflow: export "path"`
                # and if found saves a copy at that location.

                for m in re.finditer(r'@noteflow:\s*export\s*("(.+)"|[^\s]+)',
                                     content[path], re.I):
                    exportPath = m.group(1)
                    if exportPath[0] == exportPath[-1] == '"':
                        exportPath = exportPath[1:-1]

                    # VARS substitution
                    for var in vars:
                        exportPath = exportPath.replace(
                            "${}$".format(var),
                            vars[var])

                    print("+ exporting to:", exportPath)
                    os.makedirs(os.path.dirname(exportPath), exist_ok=True)
                    with open(exportPath, "w", encoding='utf8') as f:
                        f.write(content[path])

                # RUN COMMANDS
                # Searches for something like `@noteflow: run "cmd"`
                # and if found runs cmd.

                for m in re.finditer(r'@noteflow:\s*run\s*("(.+)"|[^\s]+)',
                                     content[path], re.I):
                    cmd = m.group(1)
                    if cmd[0] == cmd[-1] == '"':
                        cmd = cmd[1:-1]

                    # VARS substitution
                    for var in vars:
                        cmd = cmd.replace(
                            "${}$".format(var),
                            vars[var])

                    print("+ running cmd:", cmd)
                    proc = QProcess(self)
                    from noteflow import MW
                    MW.message("Running command: " + cmd,
                               overwrite="bookCommand")
                    proc.finished.connect(MW.processFinished)
                    proc.start(cmd)
                    t = QTimer()
                    t.setSingleShot(True)
                    t.setInterval(10000)
                    t.proc = proc
                    t.timeout.connect(self.killProc)
                    t.start()
                    self._cmdTimers.append(t)

        # Removing old content
        for path in oldContent:
            if not path in content:
                # We need to remove that file
                filename = os.path.join(self.path, path)
                os.remove(filename)

        # Removing empty folders, for the sake of cleanliness
        for root, dirs, files in os.walk(self.path):
            try:
                os.removedirs(root)
            except:
                pass

        # Write settings
        filename = os.path.join(self.path, ".NOTEFLOW")
        s = QSettings(filename, QSettings.IniFormat)
        s.setValue("Format", "1")
        s.setValue("Name", self.name)
        s.setValue("Tags", self.saveTags())
        s.setValue("Exclude", self.saveWords())

        self._content = content
        return changed

    def killProc(self):
        """
        Used to set a timeout for the run command maccro.
        """
        proc = self.sender().proc
        if not proc.state() == QProcess.Running:
            return
        proc.kill()
        try:
            print("> Output:")
            print(str(proc.readAllStandardOutput(), encoding="utf-8"))
            print("-------")
            print("> Error:")
            print(str(proc.readAllStandardError(), encoding="utf-8"))
        except UnicodeDecodeError:
            print(">> Error: can't decode error output.")
        self._cmdTimers.remove(self.sender())

    def saveTags(self):
        from noteflow import MW
        tags = []
        for t in MW.tags:
            n = [n for n in self.notes if t.text.lower() in n.tags()]
            if len(n):
                tags.append(t.toString())
        return "\n".join(tags)

    def saveWords(self):
        from noteflow import MW
        words = []
        for w in MW.hiddenWords:
            n = [n for n in self.notes if w.lower() in n.words()]
            if len(n):
                words.append(w)
        return ",".join(words)
