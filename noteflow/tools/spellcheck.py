#!/usr/bin/env python
# --!-- coding: utf8 --!--

import sys, os
# On ajoute le module grammalecte dans le path pour pouvoir le charger
sys.path.insert(0, os.path.join(os.getcwd(), "libs/grammalecte"))

import json

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


def spellcheckFromFileToJSON(text):
    """
    Spellchecks from file and returns a json object.
    """

    content = ""
    # file processing
    bComma = False

    content += """{{
                    "grammalecte": "{version}",
                    "lang": "{lang}",
                    "data" : [
             """.format(
                 version=GC.gce.version,
                 lang=GC.gce.lang,
                 )

    for i, txt, lLineSet in generateParagraphFromFile(text, False): #bConcatLines

        txt = GC.generateParagraphAsJSON(
                    i, txt,
                    bContext=True,
                    bEmptyIfNoErrors=True,
                    bSpellSugg=True,
                    bReturnText=False,
                    lLineSet=lLineSet)

        if txt:
            if bComma:
                content += ",\n"
            content += txt
            bComma = True

    content += "\n]}\n"

    return json.loads(content)

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
