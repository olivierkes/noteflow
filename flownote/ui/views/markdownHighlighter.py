#!/usr/bin/python
# -*- coding: utf-8 -*-

# Highlighter based on GhostWriter. GPLV3+.

import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from flownote.ui.views.markdownTokenizer import *
from flownote.ui.views.markdownEnums import MarkdownState as MS
from flownote.ui.views.markdownEnums import MarkdownTokenType as MTT
from flownote.ui.views.markdownEnums import BlockquoteStyle as BS

GW_FADE_ALPHA = 140


class MarkdownHighlighter(QSyntaxHighlighter):
    
    highlightBlockAtPosition = pyqtSignal(int)
    headingFound = pyqtSignal(int, str, QTextBlock)
    headingRemoved = pyqtSignal(int)

    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor)
        
        #default values
        self.editor = editor
        self.tokenizer = MarkdownTokenizer()
        #self.dictionary = DictionaryRef(DictionaryManager.instance().requestDictionary())
        self.spellCheckEnabled = False
        #self.typingPaused = True
        self.inBlockquote = False
        self.defaultTextColor = QColor(Qt.black)
        self.backgroundColor = QColor(Qt.white)
        self.markupColor = QColor(Qt.black)
        self.linkColor = QColor(Qt.blue)
        self.spellingErrorColor = QColor(Qt.red)
        self.blockquoteStyle = BS.BlockquoteStyleFancy
        
        # Settings
        self.useUndlerlineForEmphasis = False
        self.highlightLineBreaks = True
        
        #self.editor.typingResumed.connect(self.onTypingResumed)
        #self.editor.typingPaused.connect(self.onTypingPaused)
        #self.headingFound.connect(self.editor.headingFound)
        #self.headingRemoved.connect(self.editor.headingRemoved)
        
        self.highlightBlockAtPosition.connect(self.onHighlightBlockAtPosition, Qt.QueuedConnection)
        # self.editor.document().textBlockRemoved.connect(self.onTextBlockRemoved)
        
        # font = QFont("Monospace", 12, QFont.Normal, False)
        font = self.document().defaultFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        self.defaultFormat = QTextCharFormat()
        self.defaultFormat.setFont(font)
        self.defaultFormat.setForeground(QBrush(self.defaultTextColor))
        
        self.colorForToken = []
        self.applyStyleToMarkup = {}
        self.emphasizeToken = {}
        self.strongToken = {}
        self.strongMarkup = {}
        self.strikethroughToken = {}
        self.fontSizeIncrease = {}
        
        self.setupTokenColors()
        
        for i in range(MTT.TokenLast):
            self.applyStyleToMarkup[i] = False
            self.emphasizeToken[i] = False
            self.strongToken[i] = False
            self.strongMarkup[i] = False
            self.strikethroughToken[i] = False
            self.fontSizeIncrease[i] = 0
            
        for i in range(MTT.TokenAtxHeading1, MTT.TokenAtxHeading6+1):
            self.applyStyleToMarkup[i] = True
        
        self.applyStyleToMarkup[MTT.TokenEmphasis] = True
        self.applyStyleToMarkup[MTT.TokenStrong] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading1] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading2] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading3] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading4] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading5] = True
        self.applyStyleToMarkup[MTT.TokenAtxHeading6] = True

        self.emphasizeToken[MTT.TokenEmphasis] = True
        self.emphasizeToken[MTT.TokenBlockquote] = False
        self.strongToken[MTT.TokenStrong] = True
        self.strongToken[MTT.TokenMention] = True
        self.strongToken[MTT.TokenAtxHeading1] = True
        self.strongToken[MTT.TokenAtxHeading2] = True
        self.strongToken[MTT.TokenAtxHeading3] = True
        self.strongToken[MTT.TokenAtxHeading4] = True
        self.strongToken[MTT.TokenAtxHeading5] = True
        self.strongToken[MTT.TokenAtxHeading6] = True
        self.strongToken[MTT.TokenSetextHeading1Line1] = True
        self.strongToken[MTT.TokenSetextHeading2Line1] = True
        self.strongToken[MTT.TokenSetextHeading1Line2] = True
        self.strongToken[MTT.TokenSetextHeading2Line2] = True
        self.strongToken[MTT.TokenTableHeader] = True
        self.strikethroughToken[MTT.TokenStrikethrough] = True

        self.setupHeadingFontSize(True)

        self.strongMarkup[MTT.TokenNumberedList] = True
        self.strongMarkup[MTT.TokenBlockquote] = True
        self.strongMarkup[MTT.TokenBulletPointList] = True
        
    def highlightBlock(self, text):
        """
        Note:  Never set the QTextBlockFormat for a QTextBlock from within the
        highlighter.  Depending on how the block format is modified, a recursive call
        to the highlighter may be triggered, which will cause the application to
        crash.
        
        Likewise, don't try to set the QTextBlockFormat outside the highlighter
        (i.e., from within the text editor).  While the application will not crash,
        the format change will be added to the undo stack.  Attempting to undo from
        that point on will cause the undo stack to be virtually frozen, since undoing
        the format operation causes the text to be considered changed, thus
        triggering the slot that changes the text formatting to be triggered yet
        again.
        """
        
        lastState = self.currentBlockState()
        self.setFormat(0, len(text), self.defaultFormat)
        
        if self.tokenizer != None:
            self.tokenizer.clear()
            block = self.currentBlock()
            nextState = MS.MarkdownStateUnknown
            previousState = self.previousBlockState()
            
            if block.next().isValid():
                nextState = block.next().userState()
                
            self.tokenizer.tokenize(text, lastState, previousState, nextState)
            self.setCurrentBlockState(self.tokenizer.getState())
            
            self.inBlockquote = self.tokenizer.getState() == MS.MarkdownStateBlockquote
            
            # STATE FORMATTING
            # FIXME: generic
            if self.currentBlockState() in [
                    MS.MarkdownStatePipeTableHeader,
                    MS.MarkdownStatePipeTableDivider,
                    MS.MarkdownStatePipeTableRow]:
                fmt = QTextCharFormat()
                f = fmt.font()
                f.setFamily("Monospace")
                fmt.setFont(f)
                self.setFormat(0, len(text), fmt)
            
            tokens = self.tokenizer.getTokens()
            
            for token in tokens:
                if token.type in [
                    MTT.TokenAtxHeading1,
                    MTT.TokenAtxHeading2,
                    MTT.TokenAtxHeading3,
                    MTT.TokenAtxHeading4,
                    MTT.TokenAtxHeading5,
                    MTT.TokenAtxHeading6,
                    MTT.TokenSetextHeading1Line1,
                    MTT.TokenSetextHeading2Line1,
                    ]:
                    self.applyFormattingForToken(token, text)
                    self.storeHeadingData(token, text)
                
                elif token.type == MTT.TokenUnknown:
                    qWarning("Highlighter found unknown token type in text block.")
                
                else:
                    self.applyFormattingForToken(token, text)
            
            if self.tokenizer.backtrackRequested():
                previous = self.currentBlock().previous()
                self.highlightBlockAtPosition.emit(previous.position())
                
        if self.spellCheckEnabled:
            self.spellCheck(text)
        
        # If the block has transitioned from previously being a heading to now
        # being a non-heading, signal that the position in the document no longer
        # contains a heading.
        
        if self.isHeadingBlockState(lastState) and \
           not self.isHeadingBlockState(self.currentBlockState()):
            self.headingRemoved.emit(self.currentBlock().position())
            
# ==============================================================================
#   SETTINGS
# ==============================================================================
            
    def setDictionary(self, dictionary):
        self.dictionary = dictionary
        if self.spellCheckEnabled:
            self.rehighlight()
    
    def increaseFontSize(self):
        self.defaultFormat.setFontPointSize(defaultFormat.fontPointSize() + 1.0)
        self.rehighlight()
    
    def decreaseFontSize(self):
        self.defaultFormat.setFontPointSize(defaultFormat.fontPointSize() - 1.0)
        self.rehighlight()
    
    def setEnableLargeHeadingSizes(self, enable):
        self.setupHeadingFontSize(enable)
        self.rehighlight()
        
    def setupHeadingFontSize(self, useLargeHeadings):
        if useLargeHeadings:
            self.fontSizeIncrease[MTT.TokenSetextHeading1Line1] = 6
            self.fontSizeIncrease[MTT.TokenSetextHeading2Line1] = 5
            self.fontSizeIncrease[MTT.TokenSetextHeading1Line2] = 6
            self.fontSizeIncrease[MTT.TokenSetextHeading2Line2] = 5
            self.fontSizeIncrease[MTT.TokenAtxHeading1] = 6
            self.fontSizeIncrease[MTT.TokenAtxHeading2] = 5
            self.fontSizeIncrease[MTT.TokenAtxHeading3] = 4
            self.fontSizeIncrease[MTT.TokenAtxHeading4] = 3
            self.fontSizeIncrease[MTT.TokenAtxHeading5] = 2
            self.fontSizeIncrease[MTT.TokenAtxHeading6] = 1
            
        else:
            self.fontSizeIncrease[MTT.TokenSetextHeading1Line1] = 0
            self.fontSizeIncrease[MTT.TokenSetextHeading2Line1] = 0
            self.fontSizeIncrease[MTT.TokenSetextHeading1Line2] = 0
            self.fontSizeIncrease[MTT.TokenSetextHeading2Line2] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading1] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading2] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading3] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading4] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading5] = 0
            self.fontSizeIncrease[MTT.TokenAtxHeading6] = 0
        
    def setUseUnderlineForEmphasis(self, enable):
        self.useUndlerlineForEmphasis = enable
        self.rehighlight()
        
    def setFont(self, fontFamily, fontSize):
        font = QFont(family=fontFamily, pointSize=fontSize, weight=QFont.Normal, italic=False)
        self.defaultFormat.setFont(font)
        self.rehighlight()
        
    def setSpellCheckEnabled(self, enabled):
        self.spellCheckEnabled = enabled
        self.rehighlight()
        
    def setBlockquoteStyle(self, style):
        self.blockquoteStyle = style
        
        if style == BS.BlockquoteStyleItalic:
            self.emphasizeToken[MT.TokenBlockquote] = True
        else:
            self.emphasizeToken[MT.TokenBlockquote] = False
        
        self.rehighlight()
        
    def setHighlightLineBreaks(self, enable):
        self.highlightLineBreaks = enable
        self.rehighlight()
        
# ==============================================================================
#   GHOSTWRITER SPECIFIC?
# ==============================================================================
            
    def onTypingResumed(self):
        self.typingPaused = False
    
    def onTypingPaused(self):
        self.typingPaused = True
        block = self.document().findBlock(self.editor.textCursor().position())
        self.rehighlightBlock(block)
        
    def onHighlightBlockAtPosition(self, position):
        block = self.document().findBlock(position)
        self.rehighlightBlock(block)
        
    def onTextBlockRemoved(self, block):
        if self.isHeadingBlockState(block.userState):
            self.headingRemoved.emit(block.position())
            
# ==============================================================================
#   SPELLCHECK
# ==============================================================================
            
    def spellCheck(self, text):
        cursorPosition = self.editor.textCursor().position()
        cursorPosBlock = self.document().findBlock(cursorPosition)
        cursorPosInBlock = -1

        if self.currentBlock() == cursorPosBlock:
            cursorPosInBlock = cursorPosition - cursorPosBlock.position()

        misspelledWord = self.dictionary.check(text, 0)

        while not misspelledWord.isNull():
            startIndex = misspelledWord.position()
            length = misspelledWord.length()

            if self.typingPaused or cursorPosInBlock != startIndex + length:
                spellingErrorFormat = self.format(startIndex)
                spellingErrorFormat.setUnderlineColor(spellingErrorColor)
                spellingErrorFormat.setUnderlineStyle(
                    qApp.stlye().styleHint(QStyle.SH_SpellCheckUnderlineStyle))

                self.setFormat(startIndex, length, spellingErrorFormat)

            startIndex += length
            misspelledWord = dictionary.check(text, startIndex)
            
# ==============================================================================
#   COLORS & FORMATTING
# ==============================================================================
            
    def setColorScheme(self, defaultTextColor, backgroundColor, markupColor,
                       linkColor, spellingErrorColor):
        self.defaultTextColor = defaultTextColor
        self.backgroundColor = backgroundColor
        self.markupColor = markupColor
        self.linkColor = linkColor
        self.spellingErrorColor = spellingErrorColor
        self.defaultFormat.setForeground(QBrush(defaultTextColor))
        self.setupTokenColors()
        self.rehighlight()
        
    def setupTokenColors(self):
        "Functions here are taken from ColorHelper in ghostwriter"
        self.colorForToken = [self.defaultTextColor for i in range(MTT.TokenLast)]
        
        fadedColor = QColor()
        
        if getLuminance(self.backgroundColor) > \
           getLuminance(self.defaultTextColor):
            fadedColor = applyAlpha(self.defaultTextColor, self.backgroundColor, GW_FADE_ALPHA)
        else:
            fadedColor = defaultTextColor.darker(130)

        markupColor = self.markupColor
        linkColor = self.linkColor
        self.colorForToken[MTT.TokenBlockquote] = fadedColor
        self.colorForToken[MTT.TokenCodeBlock] = fadedColor
        self.colorForToken[MTT.TokenVerbatim] = fadedColor
        self.colorForToken[MTT.TokenHtmlTag] = markupColor
        self.colorForToken[MTT.TokenHtmlEntity] = markupColor
        self.colorForToken[MTT.TokenAutomaticLink] = linkColor
        self.colorForToken[MTT.TokenInlineLink] = linkColor
        self.colorForToken[MTT.TokenReferenceLink] = linkColor
        self.colorForToken[MTT.TokenReferenceDefinition] = linkColor
        self.colorForToken[MTT.TokenImage] = linkColor
        self.colorForToken[MTT.TokenMention] = linkColor
        self.colorForToken[MTT.TokenHtmlComment] = markupColor
        self.colorForToken[MTT.TokenHorizontalRule] = markupColor
        self.colorForToken[MTT.TokenGithubCodeFence] = markupColor
        self.colorForToken[MTT.TokenPandocCodeFence] = markupColor
        self.colorForToken[MTT.TokenCodeFenceEnd] = markupColor
        self.colorForToken[MTT.TokenSetextHeading1Line2] = markupColor
        self.colorForToken[MTT.TokenSetextHeading2Line2] = markupColor
        self.colorForToken[MTT.TokenTableDivider] = markupColor
        self.colorForToken[MTT.TokenTablePipe] = markupColor

# ==============================================================================
#   ACTUAL FORMATTING
# ==============================================================================

    def applyFormattingForToken(self, token, text):
        if token.type != MTT.TokenUnknown:
            tokenType = token.type
            format = self.format(token.position)
            tokenColor = QColor(self.colorForToken[tokenType])

            ## Debug
            #print("{}\n{}{}{}{}".format(
                #text,
                #" "*token.position,
                #"^"*token.openingMarkupLength,
                #str(token.type).center(token.length - token.openingMarkupLength - token.closingMarkupLength, "-"),
                #"^" * token.closingMarkupLength)
            #)
            
            if self.inBlockquote and token.type != MTT.TokenBlockquote:
                #tokenColor = applyAlpha(tokenColor, self.backgroundColor, GW_FADE_ALPHA)
                pass
            if self.highlightLineBreaks and token.type == MTT.TokenLineBreak:
                format.setBackground(QBrush(self.markupColor))
                
            format.setForeground(QBrush(tokenColor))
            
            if self.strongToken[tokenType]:
                format.setFontWeight(QFont.Bold)
                
            if self.emphasizeToken[tokenType]:
                if self.useUndlerlineForEmphasis and tokenType != MTT.TokenBlockquote:
                    format.setFontUnderline(True)
                else:
                    format.setFontItalic(True)
            
            if self.strikethroughToken[tokenType]:
                format.setFontStrikeOut(True)
            
            format.setFontPointSize(format.fontPointSize() +
                self.fontSizeIncrease[tokenType])
            
            # FIXME: generic thing for the font
            if token.type in [MTT.TokenVerbatim,
                              MTT.TokenSetextHeading1Line1, MTT.TokenSetextHeading1Line2,
                              MTT.TokenSetextHeading2Line1, MTT.TokenSetextHeading2Line2]:
                f = format.font()
                f.setFamily("Monospace")
                format.setFont(f)
                

            # FIXME: add superscript and subscript (^n^, ~n~)
            #        format.setVerticalAlignment(format.AlignSuperScript)

            # MARKUP FORMAT

            markupFormat = QTextCharFormat()
            
            if self.applyStyleToMarkup[tokenType] and \
               not self.emphasizeToken[tokenType] or \
               not self.useUndlerlineForEmphasis:
                markupFormat = QTextCharFormat(format)
                
            else:
                markupFormat = self.format(token.position)
            
            adjustedMarkupColor = QColor(self.markupColor)
            if self.inBlockquote and token.type != MTT.TokenBlockquote:
                adjustedMarkupColor = applyAlpha(adjustedMarkupColor, self.backgroundColor, GW_FADE_ALPHA)

            markupFormat.setForeground(QBrush(adjustedMarkupColor))
            if self.strongMarkup[tokenType]:
                markupFormat.setFontWeight(QFont.Bold)
            
            if token.openingMarkupLength > 0:
                if token.type == MTT.TokenBlockquote and \
                   self.blockquoteStyle == BS.BlockquoteStyleFancy:
                    markupFormat.setBackground(QBrush(adjustedMarkupColor))
                    text = self.currentBlock().text()
                    
                    for i in range(token.position, token.openingMarkupLength):
                        if text[i] != " ":
                            self.setFormat(i, 1, markupFormat)
                else:
                    self.setFormat(token.position, token.openingMarkupLength, 
                                   markupFormat)
            
            self.setFormat(
                token.position + token.openingMarkupLength,
                token.length - token.openingMarkupLength - token.closingMarkupLength,
                format)
            
            if token.closingMarkupLength > 0:
                self.setFormat(
                    token.position + token.length - token.closingMarkupLength,
                    token.closingMarkupLength,
                    markupFormat)
        
        else:
            qWarning("MarkdownHighlighter.applyFormattingForToken() was passed in a "
                     "token of unknown type.")
    
    def storeHeadingData(self, token, text):
        if token.type in [
                MTT.TokenAtxHeading1,
                MTT.TokenAtxHeading2,
                MTT.TokenAtxHeading3,
                MTT.TokenAtxHeading4,
                MTT.TokenAtxHeading5,
                MTT.TokenAtxHeading6]:
            level = token.type - MTT.TokenAtxHeading1 + 1
            s = token.position + token.openingMarkupLength
            l = token.length - token.openingMarkupLength - token.closingMarkupLength
            headingText = text[s:s+l].strip()
            
        elif token.type == MTT.TokenSetextHeading1Line1:
            level = 1
            headingText = text
            
        elif token.type == MTT.TokenSetextHeading2Line1:
            level = 2
            headingText = text
        
        else:
            qWarning("MarkdownHighlighter.storeHeadingData() encountered" + 
                     " unexpected token:".format(token.getType()))
            return

        # FIXME: TypeError: could not convert 'TextBlockData' to 'QTextBlockUserData'
        # blockData = self.currentBlockUserData()
        # if blockData is None:
        #     blockData = TextBlockData(self.document(), self.currentBlock())
        #
        # self.setCurrentBlockUserData(blockData)
        self.headingFound.emit(level, headingText, self.currentBlock())
            
    def isHeadingBlockState(self, state):
        return state in [
            MS.MarkdownStateAtxHeading1,
            MS.MarkdownStateAtxHeading2,
            MS.MarkdownStateAtxHeading3,
            MS.MarkdownStateAtxHeading4,
            MS.MarkdownStateAtxHeading5,
            MS.MarkdownStateAtxHeading6,
            MS.MarkdownStateSetextHeading1Line1,
            MS.MarkdownStateSetextHeading2Line1,
                ]


def getLuminance(color):
    return (0.30 * color.redF()) + \
           (0.59 * color.greenF()) + \
           (0.11 * color.blueF())


def applyAlphaToChannel(foreground, background, alpha):
    return (foreground * alpha) + (background * (1.0 - alpha))


def applyAlpha(foreground, background, alpha):
    blendedColor = QColor(0, 0, 0)
    normalizedAlpha = alpha / 255.0
    blendedColor.setRed(applyAlphaToChannel(
        foreground.red(), background.red(), normalizedAlpha))
    blendedColor.setGreen(applyAlphaToChannel(
        foreground.green(), background.green(), normalizedAlpha))
    blendedColor.setBlue(applyAlphaToChannel(
        foreground.blue(), background.blue(), normalizedAlpha))
    return blendedColor


class TextBlockData(QObject, QTextBlockUserData):
    def __init__(self, document, block):
        QObject.__init__(self)
        QTextBlockUserData.__init__(self)

        self.document = document
        # Parent text block.  For use with fetching the block's document
        # position, which can shift as text is inserted and deleted.
        self.blockRef = block
        self.wordCount = 0
        self.alphaNumericCharacterCount = 0
        self.sentenceCount = 0
        self.lixLongWordCount = 0
        self.blankLine = True

    # FIXME: the destructor runs TextDocument.notifyTextBlockRemoved().
    #       TextDocument is a custom QTextDocument in GhostWriter
