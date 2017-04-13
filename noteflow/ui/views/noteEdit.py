#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
from noteflow import functions as F
from noteflow.ui.views.markdownHighlighter import MarkdownHighlighter
from noteflow.ui.views.markdownEnums import MarkdownState as MS
#from noteflow.ui.views.markdownTokenizer import MarkdownTokenizer as MT


class noteEdit(QPlainTextEdit):
    
    blockquoteRegex = QRegExp("^ {0,3}(>\\s*)+")
    listRegex = QRegExp("^(\\s*)([+*-]|([0-9a-z])+([.\)]))(\\s+)")
    taskListRegex = QRegExp("^\\s*[-*+] \\[([x ])\\]\\s+")
    
    statsChanged = pyqtSignal(int, int, int, bool)
    # word, chars, chars no spaces, selection
    
    def __init__(self, parent=None, highlighting=True):
        QPlainTextEdit.__init__(self, parent)
        self.note = None
        self.textChanged.connect(self.updateNote)
        self.setEnabled(False)
        
        f = QFont("Sans", 11)
        self.setFont(f)
        self.document().setDefaultFont(f)
        
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
            
        # Statistics
        self.statsTimer = QTimer()
        self.statsTimer.setInterval(300)
        self.statsTimer.setSingleShot(True)
        self.statsTimer.timeout.connect(self.onDocChanged)
        self.document().contentsChanged.connect(self.statsTimer.start)
        self.selectionChanged.connect(self.onSelChanged)
        

# ==============================================================================
#   KEYS
# ==============================================================================

    def keyPressEvent(self, event):
        k = event.key()
        m = event.modifiers()
        cursor = self.textCursor()
        #QPlainTextEdit.keyPressEvent(self, event)
        
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
                QPlainTextEdit.keyPressEvent(self, event)
        elif k == Qt.Key_Tab:
            #self.indentText()
            # FIXME
            QPlainTextEdit.keyPressEvent(self, event)
        elif k == Qt.Key_Backtab:
            #self.unindentText()
            # FIXME
            QPlainTextEdit.keyPressEvent(self, event)
            
        else:
            QPlainTextEdit.keyPressEvent(self, event)
    
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
        if note is not None:
            self.note = note
            self.setPlainText(note.wholeText())
            self.setEnabled(True)
        else:
            self.note = None
            self.setEnabled(False)
            self.setPlainText("")
            
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