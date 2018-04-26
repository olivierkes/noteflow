#!/usr/bin/env python
# --!-- coding: utf8 --!--

import sys, os
# On ajoute le module grammalecte dans le path pour pouvoir le charger
sys.path.insert(0, os.path.join(os.getcwd(), "libs/grammalecte"))

import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import noteflow.functions as F
import libs.grammalecte.grammalecte

import libs.grammalecte.grammalecte as G
import libs.grammalecte.grammalecte.text as txt
from libs.grammalecte.grammalecte.graphspell.echo import echo

GC = G.GrammarChecker("fr")
oSpellChecker = GC.getSpellChecker()
oLexicographer = GC.getLexicographer()
oTextFormatter = GC.getTextFormatter()

CONCAT_LINES = True  # concatenate lines not separated by an empty paragraph

class spellcheckThreadManager(QObject):

    _threads = []

    @classmethod
    def getUID(cls):
        i = 0
        uids = [t.uid for t in cls._threads]
        while i in uids:
            i += 1
        return i

    @classmethod
    def spellcheckBlockToJSON(cls, block):
        """
        Spellchecks from file and returns a json object.
        """
        uid = cls.getUID()
        sct = spellcheckThread(block, uid)
        sct.spellchecked.connect(cls.spellcheckFinished)
        cls._threads.append(sct)

        sct.start()

    @classmethod
    def spellcheckFinished(cls, uid, JSONData):
        """
        JSONData is a json object
        """
        # thread = cls._threads[uid]
        thread = [t for t in cls._threads if t.uid == uid]

        if thread:
            thread = thread[0]
        else:
            return

        JSONData = """{{
                        "grammalecte": "{version}",
                        "lang": "{lang}",
                        "data" : [{data}]
                       }}""".format(
                                 version=GC.gce.version,
                                 lang=GC.gce.lang,
                                 data=JSONData,
                                 )

        # cls._threads.pop(thread.uid)
        cls._threads.remove(thread)

        from noteflow import MW
        MW.text.spellcheckBlockFromJSON(thread.block, json.loads(JSONData))

class spellcheckThread(QThread):

    # dict is a json object
    spellchecked = pyqtSignal(int, str)

    def __init__(self, block, uid):
        QThread.__init__(self)
        self.block = block
        self.concatLines = False
        self.uid = uid
        self.text = block.text()

    def run(self):

        text = self.block.text()
        bComma = False
        data = ""

        for i, txt, lLineSet in generateParagraphFromFile(text, self.concatLines): #bConcatLines

            try:
                txt = GC.generateParagraphAsJSON(
                        i, txt,
                        bContext=True,
                        bEmptyIfNoErrors=True,
                        bSpellSugg=True,
                        bReturnText=False,
                        lLineSet=lLineSet)
            except AttributeError:
                print("Spellcheck: Attribute error.")
                txt = ""
                return

            if txt:
                if bComma:
                    data += ",\n"
                data += txt
                bComma = True

        self.spellchecked.emit(self.uid, data)

###############################################################################
# From grammalecte-cli.py.
###############################################################################

def generateParagraphFromFile (text, bConcatLines=False):
    """
    generator: returns text by tuple of (iParagraph, sParagraph, lLineSet).
    """
    if not bConcatLines:
        for iParagraph, sLine in enumerate(text.split("\n"), 1):
            yield iParagraph, sLine, None
    else:
        lLine = []
        iParagraph = 1
        for iLine, sLine in enumerate(text.split("\n"), 1):
            if sLine.strip():
                lLine.append((iLine, sLine))
            elif lLine:
                sText, lLineSet = txt.createParagraphWithLines(lLine)
                yield iParagraph, sText, lLineSet
                lLine = []
            iParagraph += 1
        if lLine:
            sText, lLineSet = txt.createParagraphWithLines(lLine)
            yield iParagraph, sText, lLineSet


def readFile (text):
    "generator: returns file line by line"
    if os.path.isfile(text):
        with open(text, "r", encoding="utf-8") as hSrc:
            for sLine in hSrc:
                yield sLine
    else:
        print("# Error: file <" + spf + ">not found.")
