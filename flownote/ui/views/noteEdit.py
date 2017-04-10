#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from flownote.ui.views.markdownHighlighter import MarkdownHighlighter
from flownote.ui.views.markdownEnums import MarkdownState as MS
#from flownote.ui.views.markdownTokenizer import MarkdownTokenizer as MT


class noteEdit(QPlainTextEdit):
    
    blockquoteRegex = QRegExp("^ {0,3}(>\\s*)+")
    listRegex = QRegExp("^(\\s*)([+*-]|([0-9a-z])+([.\)]))(\\s+)")
    taskListRegex = QRegExp("^\\s*[-*+] \\[([x ])\\]\\s+")
    
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
    
    def comment(self):
        cursor = self.textCursor()
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
        cursor.movePosition(QTextCursor.StartOfBlock)
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        cursor.insertText(text2)
    
    def insertFormattingMarkup(self, markup):
        cursor = self.textCursor()
        
        # Select begining and end of words
        end = cursor.selectionEnd()
        cursor.movePosition(QTextCursor.StartOfWord)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        
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