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
import grammalecte as G
import grammalecte.text as txt
from grammalecte.graphspell.echo import echo

GC = G.GrammarChecker("fr")
oSpellChecker = GC.getSpellChecker()
oLexicographer = GC.getLexicographer()
oTextFormatter = GC.getTextFormatter()

CONCAT_LINES = True  # concatenate lines not separated by an empty paragraph

# SETTING OPTIONS

# Uncomment to list options
# print(GC.gce.displayOptions("fr"))

options = {
    "apos":   False,   # Apostrophe typographique
    "bs":     True,    # Populaire
    "chim":   False,   # Chimie [!]
    "conf":   True,    # Confusions et faux-amis
    "conj":   True,    # Conjugaisons
    "date":   True,    # Validité des dates
    "esp":    False,   # Espaces surnuméraires
    "gn":     True,    # Accords (genre et nombre)
    "html":   False,   # ?
    "idrule": False,   # Identifiant des règles de contrôle [!]
    "imp":    True,    # Impératif
    "infi":   True,    # Infinitif
    "inte":   True,    # Interrogatif
    "latex":  False,   # ?
    "liga":   True,   # Signaler ligatures typographiques
    "maj":    True,    # Majuscules
    "mapos":  False,   # Apostrophe manquante après lettres isolées [!]
    "mc":     True,   # Mots composés [!]
    "nbsp":   False,    # Espaces insécables
    "neg":    False,   # Adverbe de négation [!]
    "nf":     True,    # Normes françaises
    "num":    True,    # Nombres
    "ocr":    False,   # Erreurs de numérisation (OCR) [!]
    "pleo":   True,    # Pléonasmes
    "ppas":   True,    # Participes passés, adjectifs
    "redon1": False,   # Répétitions dans le paragraphe [!]
    "redon2": True,   # Répétitions dans la phrase [!]
    "sgpl":   True,    # Pluriels (locutions)
    "tab":    False,   # Tabulations surnuméraires
    "tu":     True,    # Traits d’union
    "typo":   False,    # Signes typographiques
    "unit":   True,    # Espaces insécables avant unités de mesure
    "virg":   True,    # Virgules
    "vmode":  True,    # Modes verbaux
}
GC.gce.setOptions(options)

class spellcheckThreadManager(QObject):

    THREAD_NUMBER = 3
    _threads = []
    _stack = []

    def __init__(self):
        # Initiate threads
        while len(self._threads) < self.THREAD_NUMBER:
            sct = spellcheckThread(parent=self)
            self._threads.append(sct)

    def spellcheckBlockToJSON(self, block):
        """
        Spellchecks from file and returns a json object.
        """

        # Add to stack
        if not block in self._stack:
            self._stack.append(block)

        # Run stack
        self.runStack()

    def getSleepingThread(self):
        """
        Returns the first non active thread.
        """
        t = [t for t in self._threads if not t.isRunning()]

        if t:
            return t[0]
        else:
            return None

    def runStack(self):

        # Start threads
        t = self.getSleepingThread()
        while t and self._stack:
            b = self._stack.pop()
            t.setBlock(b)
            t.start()
            t = self.getSleepingThread()

    def spellcheckFinished(self, JSONData, block):
        """
        JSONData is a json object
        """

        JSONData = """{{
                        "grammalecte": "{version}",
                        "lang": "{lang}",
                        "data" : [{data}]
                       }}""".format(
                                 version=GC.gce.version,
                                 lang=GC.gce.lang,
                                 data=JSONData,
                                 )

        from noteflow import MW
        MW.text.spellcheckBlockFromJSON(block, json.loads(JSONData))

        # Continue to spellcheck stack
        self.runStack()

class spellcheckThread(QThread):

    # dict is a json object
    spellchecked = pyqtSignal(str)

    def __init__(self, block=None, parent=None):
        QThread.__init__(self)
        self.block = block
        self.concatLines = False
        self.parent = parent

    def setBlock(self, block):
        self.block = block

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

        # self.spellchecked.emit(data)
        if self.parent:
            self.parent.spellcheckFinished(data, self.block)


STM = spellcheckThreadManager()

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
