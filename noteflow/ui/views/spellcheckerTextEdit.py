#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
import json
from noteflow import functions as F
from noteflow.tools.spellcheck import STM as SC

class spellcheckerNoteEdit(QPlainTextEdit):

    def __init__(self, parent=None, highlighting=True):
        QPlainTextEdit.__init__(self, parent)

        # Spellchecker
        self._autoSpellCheck = False

        # Tooltip
        lbl = QLabel(self)
        lbl.setWordWrap(True)
        lbl.setMaximumWidth(400)
        lbl.hide()
        self.spellcheckTooltip = lbl

        # Timer
        tmr = QTimer()
        tmr.setSingleShot(True)
        tmr.timeout.connect(self.spellcheckTooltip.hide)
        tmr.setInterval(50)
        self.timerHideTooltip = tmr

        # Clickable things
        self.spellRects = []
        self.textChanged.connect(self.updateSpellcheckRects)
        self.document().documentLayoutChanged.connect(self.updateSpellcheckRects)
        self.cursorPositionChanged.connect(self.updateSpellcheckRects)
        self.setMouseTracking(True)

        # Track cursor movements
        self.cursorPositionChanged.connect(self.cursorIsMoving)
        self._cursorLastBlock = None

# ==============================================================================
#   SPELLCHECK
# ==============================================================================

    def setAutoSpellcheck(self, value):
        """
        Enables auto spellcheck.
        """
        if self._autoSpellCheck != value:
            self._autoSpellCheck = value
            # self.highlighter.setSpellCheckEnabled(value)
            if not self._autoSpellCheck:
                self.clearSpellcheck()

    def spellcheck(self):
        """
        Runs spellcheck on the whole document.
        """
        if self.note:
            b = self.document().begin()
            while b.isValid():
                self.spellcheckBlock(b)
                b = b.next()

    def clearSpellcheck(self):
        self.spellRects = []
        self.setExtraSelections([])

    def removeExtraSelectionsFromBlock(self, block):
        selections = []
        oldSel = self.extraSelections()
        for es in self.extraSelections():
            if not block.contains(es.cursor.position()):
                selections.append(es)
            else:
                self.spellRects = [r for r in self.spellRects
                                   if r.extraSelection.cursor != es.cursor]

        if oldSel != selections:
            self.setExtraSelections(selections)

    def spellcheckBlock(self, block=None):

        if block is None:
            block = self.textCursor().block()

        j = SC.spellcheckBlockToJSON(block)

    def spellcheckBlockFromJSON(self, block, JSONData):
        """
        """
        # print(json.dumps(JSONData, indent=4))

        text = block.text()
        blockStart = block.position()

        # Keep only extraSelections from other blocks
        self.removeExtraSelectionsFromBlock(block)

        if not JSONData["data"]:
            return

        # Variables
        fmtGrammar = QTextCharFormat()
        fmtGrammar.setBackground(QBrush(QColor(220,220,250)))
        fmtOrth = QTextCharFormat()
        fmtOrth.setBackground(QBrush(QColor(250,220,220)))

        selections = self.extraSelections()
        objects = []

        for _type, fmt in [("lGrammarErrors", fmtGrammar),
                           ("lSpellingErrors", fmtOrth)]:

            for i in JSONData["data"][0][_type]:

                cursor = self.textCursor()
                cursor.setPosition(blockStart + i["nStart"])
                cursor.setPosition(blockStart + i["nEnd"], QTextCursor.KeepAnchor)

                selection = QTextEdit.ExtraSelection()
                selection.format = fmt
                selection.cursor = cursor
                selections.append(selection)

                rect = self.getCursorBoundingRect(cursor)
                message = ("Orthographe:" if _type == "lSpellingErrors"
                           else i.get("sMessage", ""))
                sct = SpellCheckThing(rect,
                                      extraSelection=selection,
                                      message=message,
                                      suggestions=i.get("aSuggestions", []),
                                      _type="G" if _type=="lGrammarErrors" else "O")

                self.spellRects.append(sct)

        self.setExtraSelections(selections)

# ==============================================================================
#   Context menu
# ==============================================================================


    class SpellAction(QAction):
        """A special QAction that returns the text in a signal.
        Used for spellckech."""

        correct = pyqtSignal(str)

        def __init__(self, *args):
            QAction.__init__(self, *args)

            self.triggered.connect(lambda x: self.correct.emit(
                    str(self.data())))

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu(event.pos())
        popup_menu.exec_(event.globalPos())

    def createStandardContextMenu(self, position):
        popup_menu = QPlainTextEdit.createStandardContextMenu(self)

        # Get Spell
        onRect = [r for r in self.spellRects if r.rect.contains(position)]

        if not onRect:
            return popup_menu

        for r in onRect:
            title = "Grammar" if r._type == "G" else "Spelling"
            spell_menu = QMenu(title, self)

            # Select Word
            self.setTextCursor(r.extraSelection.cursor)

            # Message
            if r.message:
                action = self.SpellAction(r.message, spell_menu)
                action.setEnabled(False)
                spell_menu.addAction(action)

            # Suggestions
            if r.suggestions:
                for word in r.suggestions:
                    action = self.SpellAction(word, spell_menu)
                    action.setData(word)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)

            # Only add the spelling suggests to the menu if not empty
            if len(spell_menu.actions()) != 0:
                popup_menu.insertSeparator(popup_menu.actions()[0])
                # Adds: suggestions
                popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)

        return popup_menu

    def correctWord(self, word):
        """
        Replaces the selected text with word.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()

        cursor.removeSelectedText()
        cursor.insertText(word)

        cursor.endEditBlock()

# ==============================================================================
#   STUFF
# ==============================================================================

    def getCursorBoundingRect(self, cursor):
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor = self.textCursor()
        cursor.setPosition(end)
        last_rect = end_rect = self.cursorRect(cursor)
        cursor.setPosition(start)
        first_rect = start_rect = self.cursorRect(cursor)
        if start_rect.y() != end_rect.y():
            cursor.movePosition(QTextCursor.StartOfLine)
            first_rect = last_rect = self.cursorRect(cursor)
            while True:
                cursor.movePosition(QTextCursor.EndOfLine)
                rect = self.cursorRect(cursor)
                if rect.y() < end_rect.y() and rect.x() > last_rect.x():
                    last_rect = rect
                moved = cursor.movePosition(QTextCursor.NextCharacter)
                if not moved or rect.y() > end_rect.y():
                    break
            last_rect = last_rect.united(end_rect)
        return first_rect.united(last_rect)

# ==============================================================================
#   INTERFACE
# ==============================================================================

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        self.updateSpellcheckRects()

    def scrollContentsBy(self, dx, dy):
        QPlainTextEdit.scrollContentsBy(self, dx, dy)
        self.updateSpellcheckRects()

    def updateSpellcheckRects(self):

        # # Update grammar rects
        for r in self.spellRects:
            cursor = r.extraSelection.cursor
            rect = self.getCursorBoundingRect(cursor)
            r.rect = rect

    def mouseMoveEvent(self, event):
        QPlainTextEdit.mouseMoveEvent(self, event)

        onRect = [r for r in self.spellRects if r.rect.contains(event.pos())]

        if not onRect:
            self.timerHideTooltip.start()
            return

        tooltip = ""
        for sct in onRect:

            tooltip += "<p><b>{msg}</b><br>{sug}</p>".format(
                msg=sct.message,
                sug=", ".join(sct.suggestions)
            )

        if tooltip:
            self.showToolTip(event.pos(), tooltip, sct._type)

    def cursorIsMoving(self):
        cursor = self.textCursor()
        bn = cursor.blockNumber()

        if (self._cursorLastBlock
             and self._autoSpellCheck
             and bn != self._cursorLastBlock):

            self.spellcheckBlock(self.document().findBlockByNumber(self._cursorLastBlock))

        self._cursorLastBlock = bn

# ==============================================================================
#   TOOLTIPS
# ==============================================================================

    def showToolTip(self, pos, msg, _type):
        lbl = self.spellcheckTooltip
        lbl.setText(msg)
        lbl.adjustSize()
        r = lbl.geometry()
        r.moveTopLeft(pos + QPoint(0, 20))
        if r.right() > self.viewport().geometry().right():
            r.moveRight(self.viewport().geometry().right())
        lbl.setGeometry(r)

        lbl.setStyleSheet("""
              background: {color};
              border-radius: 5px;
              border: 1px solid black;
              """.format(
                 color="#CCCCFF" if _type == "G" else "#FFCCCC"
              ))

        lbl.show()
        self.timerHideTooltip.stop()

    # def paintEvent(self, event):
    #     QPlainTextEdit.paintEvent(self, event)
    #
    #     # Debug: paint rects
    #     painter = QPainter(self.viewport())
    #     painter.setPen(Qt.gray)
    #     for r in self.spellRects:
    #         painter.drawRect(r.rect)

class SpellCheckThing:
    def __init__(self, rect, extraSelection, message="", suggestions=[], _type=""):
        self.rect = rect
        self.extraSelection = extraSelection
        self.message = message
        self.suggestions = suggestions
        self._type = _type  # "G" / "O"
