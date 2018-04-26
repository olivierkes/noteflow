#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
from noteflow import functions as F
from noteflow.ui.views.spellcheckerTextEdit import spellcheckerNoteEdit
from noteflow.ui.views.markdownHighlighter import MarkdownHighlighter
from noteflow.ui.views.markdownEnums import MarkdownState as MS
from noteflow.ui.views.markdownTokenizer import MarkdownTokenizer as MT
from noteflow.ui.views.noteCompleter import noteCompleter

class noteEdit(spellcheckerNoteEdit):

    blockquoteRegex = QRegExp("^ {0,3}(>\\s*)+")
    listRegex = QRegExp("^(\\s*)([+*-]|([0-9a-z])+([.\)]))(\\s+)")
    taskListRegex = QRegExp("^\\s*[-*+] \\[([x ])\\]\\s+")
    noteRef = QRegExp(r"(\d{4}-\d{2}-\d{2})/(.+)")
    inlineLinkRegex = QRegExp("\\[([^\n]+)\\]\\(([^\n]+)\\)")
    inlineLinkRegex.setMinimal(True)
    imageRegex = QRegExp("!\\[([^\n]*)\\]\\(([^\n]+)\\)")
    imageRegex.setMinimal(True)
    automaticLinkRegex = QRegExp("(<([a-zA-Z]+\\:[^\n]+)>)|(<([^\n]+@[^\n]+)>)")
    automaticLinkRegex.setMinimal(True)

    statsChanged = pyqtSignal(int, int, int, bool)
    noteChanged = pyqtSignal(int)
    structureChanged = pyqtSignal()
    headingFound = pyqtSignal(int, str, QTextBlock)
    headingRemoved = pyqtSignal(int)
    openRef = pyqtSignal(str, str)
    # word, chars, chars no spaces, selection

    def __init__(self, parent=None, highlighting=True):
        spellcheckerNoteEdit.__init__(self, parent)
        self.note = None
        self.setEnabled(False)

        f = QFont("Sans", 11)
        self.setFont(f)
        self.document().setDefaultFont(f)

        # Highlighter
        self.highlighter = None
        if highlighting:
            self.highlighter = MarkdownHighlighter(self)
            self.highlighter.setColorScheme(
                QColor(Qt.black),
                QColor(Qt.white),
                QColor(Qt.lightGray),
                QColor(Qt.blue),
                QColor(Qt.red)
            )

        # Tag Completer
        self.tagCompleter = QCompleter()
        self.tagModel = QStringListModel()
        self.tagCompleter.setModel(self.tagModel)
        self.tagCompleter.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.tagCompleter.setWrapAround(False)
        self.tagCompleter.setWidget(self)
        self.tagCompleter.setCompletionMode(QCompleter.PopupCompletion)
        self.tagCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.tagCompleter.setFilterMode(Qt.MatchContains)
        self.tagCompleter.activated.connect(self.insertTagCompletion)

        # Note Completer
        self.noteCompleter = noteCompleter(self)
        self.noteCompleter.activated.connect(self.insertNoteCompletion)

        # Statistics
        self.statsTimer = QTimer()
        self.statsTimer.setInterval(300)
        self.statsTimer.setSingleShot(True)
        self.statsTimer.timeout.connect(self.onDocChanged)
        self.document().contentsChanged.connect(self.statsTimer.start)
        self.selectionChanged.connect(self.onSelChanged)

        # Update Note Timer
        self.updateTimer = QTimer()
        self.updateTimer.setInterval(300)
        self.updateTimer.setSingleShot(True)
        self.updateTimer.timeout.connect(self.updateNote)
        self.textChanged.connect(self.updateTimer.start)

        # Clickable things
        self.clickRects = []
        self.textChanged.connect(self.getClickRects)
        self.document().documentLayoutChanged.connect(self.getClickRects)
        self.setMouseTracking(True)

# ==============================================================================
#   TAG COMPLETER
# ==============================================================================

    def updateCompleterWords(self):
        from noteflow import MW
        tags = MW.allTags()
        words = sorted(tags.keys(), key=lambda k: tags[k], reverse=True)
        words = ["{} ({}×)".format(w, tags[w]) for w in words]
        self.tagModel.setStringList(words)

    def tagUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        a, b = tc.anchor(), tc.position()
        tc.setPosition(max(0, a-1))
        tc.setPosition(b, tc.KeepAnchor)
        return tc.selectedText(), a-1

    def insertTagCompletion(self, completion):
        # Remove the parenthesis (42×) at the end
        completion = re.sub(r"^(#.*) \(.*\)$", "\\1", completion)

        if self.tagCompleter.widget() != self:
            return;
        tc = self.textCursor()
        #extra = len(completion) - len(self.tagCompleter.completionPrefix())
        #tc.movePosition(QTextCursor.Left)
        #tc.movePosition(QTextCursor.EndOfWord)
        #tc.insertText(completion[-extra:])
        tc.movePosition(QTextCursor.EndOfWord)
        tc.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        tc.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        tc.insertText(completion)
        self.setTextCursor(tc)

# ==============================================================================
#   NOTECOMPLETER
# ==============================================================================

    def insertNoteCompletion(self, note):
        tc = self.textCursor()
        txt = "[{title}](n://{date}/{title})".format(title=note.title,
                                                     date=note.date)
        tc.insertText(txt)
        self.setTextCursor(tc)

    def popupNoteCompleter(self):
        if self.noteCompleter:
            cr = self.cursorRect()
            cr.moveTopLeft(self.mapToGlobal(cr.bottomLeft()))
            cr.setWidth(self.noteCompleter.sizeHint().width())
            cr.setHeight(self.noteCompleter.sizeHint().height())
            self.noteCompleter.setGeometry(cr)
            self.noteCompleter.popup(self.textUnderCursor(select=True))

    def textUnderCursor(self, select=False):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        if select:
            self.setTextCursor(tc)
        return tc.selectedText()
# ==============================================================================
#   KEYS
# ==============================================================================

    def keyPressEvent(self, event):
        k = event.key()
        m = event.modifiers()
        cursor = self.textCursor()
        #spellcheckerNoteEdit.keyPressEvent(self, event)

        if (self.tagCompleter and self.tagCompleter.popup().isVisible()
            or self.noteCompleter.isVisible()):
            # The following keys are forwarded by the completer to the widget
            if event.key() in [Qt.Key_Enter, Qt.Key_Return,
                               Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]:
                event.ignore()
                # Let the completer do default behavior
                return

        # Note completer
        isShortcut = (event.modifiers() == Qt.ControlModifier and \
                      event.key() == Qt.Key_Space)

        if self.noteCompleter and isShortcut:
            self.popupNoteCompleter()
        else:
            self.noteCompleter.setVisible(False)

        if k == Qt.Key_Return:
            if not cursor.hasSelection():
                if m & Qt.ShiftModifier:
                    # Insert Markdown-style line break
                    cursor.insertText("  ")

                if m & Qt.ControlModifier:
                    cursor.insertText("\n")
                else:
                    self.handleCarriageReturn()
            else:
                spellcheckerNoteEdit.keyPressEvent(self, event)
        elif k == Qt.Key_Tab:
            #self.indentText()
            # FIXME
            spellcheckerNoteEdit.keyPressEvent(self, event)
        elif k == Qt.Key_Backtab:
            #self.unindentText()
            # FIXME
            spellcheckerNoteEdit.keyPressEvent(self, event)

        else:
            spellcheckerNoteEdit.keyPressEvent(self, event)

        # Text under cursor
        completionPrefix, start = self.tagUnderCursor()
        start -= self.textCursor().block().position()
        pos = self.textCursor().position() - self.textCursor().block().position() - len(completionPrefix)
        if (pos != 0 and completionPrefix and completionPrefix[0] == "#"
            and start == pos):

            # Popup completer
            if completionPrefix != self.tagCompleter.completionPrefix():
                self.updateCompleterWords()
                self.tagCompleter.setCompletionPrefix(completionPrefix[1:])
                self.tagCompleter.popup().setCurrentIndex(
                    self.tagCompleter.completionModel().index(0, 0))

            cr = QRect(self.cursorRect())
            cr.setWidth(self.tagCompleter.popup().sizeHintForColumn(0)
                        + self.tagCompleter.popup().verticalScrollBar().sizeHint().width())
            self.tagCompleter.complete(cr)

        else:
            self.tagCompleter.popup().hide()

    # Again, thanks to GhostWriter, mainly
    def handleCarriageReturn(self):
        autoInsertText = "";
        cursor = self.textCursor()
        endList = False
        moveBack = False
        text = cursor.block().text()

        if cursor.positionInBlock() < cursor.block().length() - 1:
            autoInsertText = self.getPriorIndentation()
            if cursor.positionInBlock() < len(autoInsertText):
                autoInsertText = autoInsertText[:cursor.positionInBlock()]

        else:
            s = cursor.block().userState()

            if s in [MS.MarkdownStateNumberedList,
                     MS.MarkdownStateBulletPointList]:
                self.listRegex.indexIn(text)
                g = self.listRegex.capturedTexts()
                    # 0 = "   a. " or "  * "
                    # 1 = "   "       "  "
                    # 2 =    "a."       "*"
                    # 3 =    "a"          ""
                    # 4 =     "."         ""
                    # 5 =      " "        " "

                # If the line of text is an empty list item, end the list.
                if len(g[0].strip()) == len(text.strip()):
                    endList = True

                # Else increment the list number
                elif g[3]:  # Numbered list
                    try: # digit
                        i = int(g[3])+1

                    except: # letter
                        i = chr(ord(g[3])+1)

                    autoInsertText = "{}{}{}{}".format(
                            g[1], i, g[4], g[5])

                else:  # Bullet list
                    autoInsertText = g[0]

                if text[-2:] == "  ":
                    autoInsertText = " " * len(autoInsertText)

            elif s == MS.MarkdownStateBlockquote:
                self.blockquoteRegex.indexIn(text)
                g = self.blockquoteRegex.capturedTexts()
                autoInsertText = g[0]

            elif s in [MS.MarkdownStateInGithubCodeFence,
                       MS.MarkdownStateInPandocCodeFence] and \
                 cursor.block().previous().userState() != s:
                autoInsertText = "\n" + text
                moveBack = True

            else:
                autoInsertText = self.getPriorIndentation()

        # Clear the list
        if endList:
            autoInsertText = self.getPriorIndentation()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            cursor.insertText(autoInsertText)
            autoInsertText = ""

        # Finally, we insert
        cursor.insertText("\n" + autoInsertText)
        if moveBack:
            cursor.movePosition(QTextCursor.PreviousBlock)
            self.setTextCursor(cursor)

        self.ensureCursorVisible()

    def getPriorIndentation(self):
        text = self.textCursor().block().text()
        l = len(text) - len(text.lstrip())
        return text[:l]

    def getPriorMarkdownBlockItemStart(self, itemRegex):
        text = self.textCursor().block().text()
        if itemRegex.indexIn(text) >= 0:
            return text[itemRegex.matchedLength():]

        return ""

# ==============================================================================
#   FORMATTING
# ==============================================================================

    def bold(self): self.insertFormattingMarkup("**")
    def italic(self): self.insertFormattingMarkup("*")
    def strike(self): self.insertFormattingMarkup("~~")
    def verbatim(self): self.insertFormattingMarkup("`")
    def superscript(self): self.insertFormattingMarkup("^")
    def subscript(self): self.insertFormattingMarkup("~")

    def selectWord(self, cursor):
        end = cursor.selectionEnd()
        cursor.movePosition(QTextCursor.StartOfWord)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)

    def selectBlock(self, cursor):
        cursor.movePosition(QTextCursor.StartOfBlock)
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)

    def comment(self):
        cursor = self.textCursor()

        # Select begining and end of words
        self.selectWord(cursor)

        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText("<!-- " + text + " -->")
        else:
            cursor.insertText("<!--  -->")
            cursor.movePosition(QTextCursor.PreviousCharacter,
                                QTextCursor.MoveAnchor, 4)
            self.setTextCursor(cursor)

    def commentLine(self):
        cursor = self.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        block = self.document().findBlock(start)
        block2 = self.document().findBlock(end)

        if True:
            # Method 1
            cursor.beginEditBlock()
            while block.isValid():
                self.commentBlock(block)
                if block == block2: break
                block = block.next()
            cursor.endEditBlock()

        else:
            # Method 2
            cursor.beginEditBlock()
            cursor.setPosition(block.position())
            cursor.insertText("<!--\n")
            cursor.setPosition(block2.position() + block2.length() - 1)
            cursor.insertText("\n-->")
            cursor.endEditBlock()

    def commentBlock(self, block):
        cursor = QTextCursor(block)
        text = block.text()
        if text[:5] == "<!-- " and \
           text[-4:] == " -->":
            text2 = text[5:-4]
        else:
            text2 = "<!-- " + text + " -->"
        self.selectBlock(cursor)
        cursor.insertText(text2)

    def insertFormattingMarkup(self, markup):
        cursor = self.textCursor()

        # Select begining and end of words
        self.selectWord(cursor)

        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd() + len(markup)
            cursor.beginEditBlock()
            cursor.setPosition(start)
            cursor.insertText(markup)
            cursor.setPosition(end)
            cursor.insertText(markup)
            cursor.endEditBlock()
            cursor.movePosition(QTextCursor.PreviousCharacter,
                                QTextCursor.KeepAnchor, len(markup))
            #self.setTextCursor(cursor)

        else:
            # Insert markup twice (for opening and closing around the cursor),
            # and then move the cursor to be between the pair.
            cursor.beginEditBlock()
            cursor.insertText(markup)
            cursor.insertText(markup)
            cursor.movePosition(QTextCursor.PreviousCharacter,
                                QTextCursor.MoveAnchor, len(markup))
            cursor.endEditBlock()
            self.setTextCursor(cursor)

    def clearFormat(self):
        cursor = self.textCursor()
        text = cursor.selectedText()
        if not text:
            self.selectBlock()
            text = cursor.selectedText()
        text = self.clearedFormat(text)
        cursor.insertText(text)

    def clearedFormat(self, text):
        # FIXME: clear also block formats
        for reg, rep, flags in [
            ("\*\*(.*?)\*\*", "\\1", None), # bold
            ("__(.*?)__", "\\1", None), # bold
            ("\*(.*?)\*", "\\1", None), # emphasis
            ("_(.*?)_", "\\1", None), # emphasis
            ("`(.*?)`", "\\1", None), # verbatim
            ("~~(.*?)~~", "\\1", None), # strike
            ("\^(.*?)\^", "\\1", None), # superscript
            ("~(.*?)~", "\\1", None), # subscript
            ("<!--(.*)-->", "\\1", re.S), # comments


            # LINES OR BLOCKS
            (r"^#*\s*(.+?)\s*", "\\1", re.M), # ATX
            (r"^[=-]*$", "", re.M), # Setext
            (r"^`*$", "", re.M), # Code block fenced
            (r"^\s*[-+*]\s*(.*?)\s*$", "\\1", re.M), # Bullet List
            (r"^\s*[0-9a-z](\.|\))\s*(.*?)\s*$", "\\2", re.M), # Bullet List
            (r"\s*[>\s]*(.*?)\s*$", "\\1", re.M), # Code block and blockquote

            ]:
            text = re.sub(reg, rep, text, flags if flags else 0)
        return text

    def clearedFormatForStats(self, text):
        # Remove stuff that musn't be counted
        # FIXME: clear also block formats
        for reg, rep, flags in [
            ("<!--.*-->", "", re.S), # comments
            ]:
            text = re.sub(reg, rep, text, flags if flags else 0)
        return text

    def titleSetext(self, level):
        cursor = self.textCursor()

        cursor.beginEditBlock()
        # Is it already a Setext header?
        if cursor.block().userState() in [
                MS.MarkdownStateSetextHeading1Line2,
                MS.MarkdownStateSetextHeading2Line2]:
            cursor.movePosition(QTextCursor.PreviousBlock)

        text = cursor.block().text()

        if cursor.block().userState() in [
                MS.MarkdownStateSetextHeading1Line1,
                MS.MarkdownStateSetextHeading2Line1]:
            # Need to remove line below
            c = QTextCursor(cursor.block().next())
            self.selectBlock(c)
            c.insertText("")

        char = "=" if level == 1 else "-"
        text = re.sub("^#*\s*(.*)\s*#*", "\\1", text)  # Removes #
        sub = char * len(text)
        text = text + "\n" + sub

        self.selectBlock(cursor)
        cursor.insertText(text)
        cursor.endEditBlock()

    def titleATX(self, level):
        cursor = self.textCursor()
        text = cursor.block().text()

        # Are we in a Setext Header?
        if cursor.block().userState() in [
                MS.MarkdownStateSetextHeading1Line1,
                MS.MarkdownStateSetextHeading2Line1]:
            # Need to remove line below
            cursor.beginEditBlock()
            c = QTextCursor(cursor.block().next())
            self.selectBlock(c)
            c.insertText("")

            self.selectBlock(cursor)
            cursor.insertText(text)
            cursor.endEditBlock()
            return

        elif cursor.block().userState() in [
                MS.MarkdownStateSetextHeading1Line2,
                MS.MarkdownStateSetextHeading2Line2]:
            cursor.movePosition(QTextCursor.PreviousBlock)
            self.setTextCursor(cursor)
            self.titleATX(level)
            return

        m = re.match("^(#+)(\s*)(.+)", text)
        if m:
            pre = m.group(1)
            space = m.group(2)
            txt = m.group(3)

            if len(pre) == level:
                # Remove title
                text = txt
            else:
                text = "#" * level + space + txt

        else:
            text = "#" * level + " " + text

        self.selectBlock(cursor)
        cursor.insertText(text)

# ==============================================================================
#   STATISTICS
# ==============================================================================

    def onDocChanged(self):
        # Update statistics !
        b = self.document().begin()
        w = 0
        c = 0
        c2 = 0
        while b.isValid():
            # Do stuff
            uData = b.userData()
            if not uData:
                uData = UserData(b, self)
                b.setUserData(uData)

            uData.countChars()
            w += uData.wordsNumber
            c += uData.charsNumber
            c2 += uData.charsNumberNoSpace
            b = b.next()

        self._statsWord = w
        self._statsChars = c
        self._statsCharsNoSpaces = c2
        self.statsChanged.emit(w, c, c2, False)

    def onSelChanged(self):
        cursor = self.textCursor()
        text = cursor.selectedText().replace("\u2029", "\n")
        text = self.clearedFormatForStats(text)
        text = "\n".join([self.clearedFormat(t) for t in text.split("\n")])
        w, c, c2 = F.stats(text)
        self.statsChanged.emit(w, c, c2, True)

# ==============================================================================
#   NOTES
# ==============================================================================

    def setNote(self, note):

        # Remember the position in the note
        if self.note is not None:
        # Ratio of scrollbar
            bar = self.verticalScrollBar()
            try:
                r = bar.value() / bar.maximum()
                self.note._posInNoteScroll = r
            except ZeroDivisionError:
                self.note._posInNoteScroll = 0

            # Cursor
            self.note._posInNoteCursor = self.textCursor().position()

            # Submit
            self.updateNote()

        if note is not None:
            self.note = note
            self.setPlainText(note.wholeText())
            self.setEnabled(True)
        else:
            self.note = None
            self.setEnabled(False)
            self.setPlainText("")

        # Restores the position of the scrollbar
        # FIXME: does not restore the proper position exactly
        #        because bar.maximum() is not the same (?!?)
        if self.note and self.note._posInNoteScroll:
            bar = self.verticalScrollBar()
            bar.setValue(self.note._posInNoteScroll * bar.maximum())
        if self.note and self.note._posInNoteCursor:
            c = self.textCursor()
            c.setPosition(self.note._posInNoteCursor)
            self.setTextCursor(c)

        self.noteChanged.emit(note)

    def updateNote(self):
        if self.note:
            self.note.setWholeText(self.toPlainText())
        else:
            if self.toPlainText():
                self.setPlainText("")
            self.setEnabled(False)

    def setHighlighted(self, words, tags):
        if self.highlighter:
            self.highlighter.setHighlighted(
                [w for w in words if len(w) >= 2],
                tags)

    def setSearched(self, expression, regExp=False, caseSensitivity=False):
        if self.highlighter:
            self.highlighter.setSearched(expression, regExp, caseSensitivity)

# ==============================================================================
#   LINKS
# ==============================================================================

    def setCursorPosition(self, position):
        t = self.textCursor()
        t.setPosition(position)
        self.setTextCursor(t)
        self.centerCursor()

# ==============================================================================
#   LINKS
# ==============================================================================

    def resizeEvent(self, event):
        spellcheckerNoteEdit.resizeEvent(self, event)
        self.getClickRects()

    def scrollContentsBy(self, dx, dy):
        spellcheckerNoteEdit.scrollContentsBy(self, dx, dy)
        self.getClickRects()

    def getClickRects(self):
        cursor = self.textCursor()
        f = self.font()
        # f.setFixedPitch(True)
        # f.setWeight(QFont.DemiBold)
        fm = QFontMetrics(f)
        refs = []

        text = self.toPlainText()
        for rx in [
                self.imageRegex,
                self.automaticLinkRegex,
                self.inlineLinkRegex,
            ]:
            pos = 0
            while rx.indexIn(text, pos) != -1:
                cursor.setPosition(rx.pos())
                r1 = self.cursorRect(cursor)
                pos = rx.pos() + rx.matchedLength()
                cursor.setPosition(pos)
                r2 = self.cursorRect(cursor)
                if r1.top() == r2.top():
                    ct = ClickThing(
                            QRect(r1.topLeft(), r2.bottomRight()),
                            rx,
                            rx.capturedTexts())
                    refs.append(ct)
                else:
                    r1.setRight(self.viewport().geometry().right())
                    refs.append(ClickThing(r1, rx, rx.capturedTexts()))
                    r2.setLeft(self.viewport().geometry().left())
                    refs.append(ClickThing(r2, rx, rx.capturedTexts()))
                    # We check for middle lines
                    cursor.setPosition(rx.pos())
                    cursor.movePosition(cursor.Down)
                    while self.cursorRect(cursor).top() != r2.top():
                        r3 = self.cursorRect(cursor)
                        r3.setLeft(self.viewport().geometry().left())
                        r3.setRight(self.viewport().geometry().right())
                        refs.append(ClickThing(r3, rx, rx.capturedTexts()))
                        cursor.movePosition(cursor.Down)

        self.clickRects = refs

    def mouseMoveEvent(self, event):
        """
        Detects and acts on images and links.
        """
        spellcheckerNoteEdit.mouseMoveEvent(self, event)

        self._lastMousePos = event.pos()

        onRect = [r for r in self.clickRects if r.rect.contains(event.pos())]
        self._lastMousePos = event.pos()

        if not onRect:
            from noteflow import MW
            qApp.restoreOverrideCursor()
            QToolTip.hideText()
            MW.hidePreviewPixmap()
            return

        ct = onRect[0]
        if not qApp.overrideCursor():
            qApp.setOverrideCursor(Qt.PointingHandCursor)

        if ct.regex == self.automaticLinkRegex:
            tooltip = ct.texts[2] or ct.texts[4]

        elif ct.regex == self.imageRegex:
            # tooltip = ct.texts[1] or ct.texts[2]
            # tooltip = "<p><b>{}</b></p><p><img src='{}'></p>".format(ct.texts[1], ct.texts[2])
            if not ct.rect.contains(self._lastMousePos):
                return
            tt = "<p><b>"+ct.texts[1]+"</b></p><p><img src='data:image/png;base64,{}'></p>"
            tooltip = None
            F.getImage(ct.texts[2], self.tooltipImage, [ct, event.pos()])

        elif ct.regex == self.inlineLinkRegex:
            tooltip = ct.texts[1] or ct.texts[2]

        if tooltip:
            tooltip = "{} (CTRL+click to open)".format(tooltip)
            QToolTip.showText(self.mapToGlobal(event.pos()), tooltip)

    def tooltipImage(self, success, reply, savedVars):
        ct, pos = savedVars

        if not ct.rect.contains(self._lastMousePos):
            # Mouse hase moved out of rect
            return

        if success:
            from noteflow import MW
            MW.previewPixmap(reply, self.mapToGlobal(pos))
            # tooltip = F.pixmapToTooltip(reply)
            # QToolTip.showText(self.mapToGlobal(pos), tooltip)

        else:
            tt = "<p>Error: {}</p>".format(reply)
            QToolTip.showText(self.mapToGlobal(pos), tt)

    def mouseReleaseEvent(self, event):
        spellcheckerNoteEdit.mouseReleaseEvent(self, event)
        onRect = [r for r in self.clickRects if r.rect.contains(event.pos())]
        if onRect and event.modifiers() & Qt.ControlModifier:
            ct = onRect[0]

            if ct.regex == self.automaticLinkRegex:
                url = ct.texts[2] or ct.texts[4]
            elif ct.regex == self.imageRegex:
                url = ct.texts[2]
            elif ct.regex == self.inlineLinkRegex:
                url = ct.texts[2]

            # Check if it's a note reference
            title = ct.texts[1]
            n = F.linkMatchedNote(title, url)
            if n:
                from noteflow import MW
                MW.openNote(n.UID)
            else:
                F.openURL(url)
                qApp.restoreOverrideCursor()

    # def paintEvent(self, event):
    #     spellcheckerNoteEdit.paintEvent(self, event)
    #
    #     # Debug: paint rects
    #     painter = QPainter(self.viewport())
    #     painter.setPen(Qt.gray)
    #     for r in self.clickRects:
    #         painter.drawRect(r.rect)

class ClickThing:
    def __init__(self, rect, regex, texts):
        self.rect = rect
        self.regex = regex
        self.texts = texts

class UserData(QTextBlockUserData):
    def __init__(self, block, editor):
        QTextBlockUserData.__init__(self)
        self.block = block
        self.editor = editor
        self.text = None
        self.wordsNumber = -1
        self.charsNumber = -1
        self.charsNumberNoSpace = -1

    def countChars(self):
        text = self.block.text()

        if text != self.text:
            t = self.editor.clearedFormat(text)
            t = self.editor.clearedFormatForStats(t)
            w, c, c2 = F.stats(t)
            self.wordsNumber = w
            self.charsNumber = c
            self.charsNumberNoSpace = c2
            self.text = text
