#!/usr/bin/python
# -*- coding: utf-8 -*-

# MarkdownHighlighter is a simple syntax highlighter for Markdown syntax.
# The initial code for MarkdownHighlighter was taken from niwmarkdowneditor by John Schember
# Copyright 2009 John Schember, Copyright 2012 Rupesh Kumar

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

'''
Highlight Markdown text
'''

import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MarkdownHighlighter(QSyntaxHighlighter):
    
    MARKDOWN_INLINE_BEAUTIFIERS = ["Bold", "uBold", "Italic", "uItalic", "CodeSpan"]
    MARKDOWN_INLINE_KEYS_REGEX = {
        'Bold': re.compile('(?P<delim>\*\*)(?P<text>.+?)(?P=delim)'),
        'uBold': re.compile('(?P<delim>__)(?P<text>[^_]{2,}?)(?P=delim)'),
         # No space at the begginning to avoid confusion with list
        'Italic': re.compile('(?P<delim>\*)(?P<text>[^\s][^*]{2,}?)(?P=delim)(?!\*)'),
        'uItalic': re.compile('(?P<delim>_)(?P<text>[^_]+?)(?P=delim)(?!_)'),
        'CodeSpan': re.compile('(?P<delim>`+)(?P<text>.+?)(?P=delim)'),
        #'Link': re.compile('(^|(?P<pre>[^!]))\[.*?\]:?[ \t]*\(?[^)]+\)?'),
        'Link': re.compile('(?<!\!)\[(?P<name>.*?)\]:?[ \t]*\(?[^)]+\)?'),
        'Image': re.compile('!\[.*?\]\(.+?\)'),
        'Html': re.compile('<.+?>')
    }
    
    MARKDOWN_LINE_KEYS_REGEX = {
        'HeaderAtx': re.compile('^\#{1,6}(.*?)\#*(\n|$)'),
        'Header': re.compile('^(.+)[ \t]*\n(=+|-+)[ \t]*\n+'),
        'CodeBlock': re.compile('^([ ]{4,}|\t).*'),
        'UnorderedList': re.compile('^\s*(\* |\+ |- )+\s*'),
        'UnorderedListStar': re.compile('^\s*(\* )+\s*'),
        'OrderedList': re.compile('^\s*(\d+\. )\s*'),
        'BlockQuote': re.compile('^\s*>+\s*'),
        'BlockQuoteCount': re.compile('^[ \t]*>[ \t]?'),
        'HR': re.compile('^(\s*(\*|-)\s*){3,}$'),
        'eHR': re.compile('^(\s*(\*|=)\s*){3,}$'),
    }

    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.parent.setTabStopWidth(self.parent.fontMetrics().width(' ')*8)

        self.defaultTheme = {
            "background-color":"#ffffff", 
            "color": "#000000", 
            "bold": {"color": "#000", "font-weight": "bold", "font-style": "normal"},  #859900
            "emphasis": {"color":"#000", "font-weight":"normal", "font-style":"italic"}, #b58900
            "link": {"color":"#cb4b16", "font-weight":"normal", "font-style":"normal"}, 
            "image": {"color":"#cb164b", "font-weight":"normal", "font-style":"normal"}, 
            "header": {"color":"#2aa198", "font-weight":"bold", "font-style":"normal"}, 
            "unorderedlist": {"color":"#dc322f", "font-weight":"normal", "font-style":"normal"}, 
            "orderedlist": {"color":"#dc322f", "font-weight":"normal", "font-style":"normal"}, 
            "blockquote": {"color":"#dc322f", "font-weight":"normal", "font-style":"normal"}, 
            "codespan": {"color":"#dc322f", "font-weight":"normal", "font-style":"normal"}, 
            "codeblock": {"color":"#ff9900", "font-weight":"normal", "font-style":"normal"}, 
            "line": {"color":"#2aa198", "font-weight":"normal", "font-style":"normal"}, 
            "html": {"color":"#c000c0", "font-weight":"normal", "font-style":"normal"}
            }
        self.setTheme(self.defaultTheme)

    def setTheme(self, theme):
        self.theme = theme
        self.MARKDOWN_KWS_FORMAT = {}

        pal = self.parent.palette()
        pal.setColor(QPalette.Base, QColor(theme['background-color']))
        self.parent.setPalette(pal)
        self.parent.setTextColor(QColor(theme['color']))
        
        format = QTextCharFormat()
        format.setForeground(Qt.lightGray)
        self.MARKDOWN_KWS_FORMAT['Delim'] = format
        
        for what, name in [
            ("bold", "Bold"), ("bold", "uBold"),
            ("emphasis", "Italic"), ("emphasis", "uItalic"),
            ("link", "Link"),
            ("image", "Image"),
            ("header", "Header"), ("header", "HeaderAtx"),
            ("unorderedlist", "UnorderedList"),
            ("orderedlist", "OrderedList"),
            ("blockquote", "BlockQuote"),
            ("codespan", "CodeSpan"),
            ("codeblock", "CodeBlock"),
            ("line", "HR"), ("line", "eHR"),
            ("html", "HTML"),            
            ]:
            
            format = QTextCharFormat()
            format.setForeground(QBrush(QColor(theme[what]['color'])))
            format.setFontWeight(QFont.Bold if theme[what]['font-weight']=='bold' else QFont.Normal)
            format.setFontItalic(True if theme[what]['font-style']=='italic' else False)
            self.MARKDOWN_KWS_FORMAT[name] = format
            
        # Customisation
        # self.MARKDOWN_KWS_FORMAT['Header'].setFontPointSize(self.parent.font().pointSize() * 1.25)
        # self.MARKDOWN_KWS_FORMAT['HeaderAtx'].setFontPointSize(self.parent.font().pointSize() * 1.25)

        self.rehighlight()

    def highlightBlock(self, text):
        if self.currentBlock().blockNumber() == 0:
            # This is the title
            bf = QTextCharFormat()
            bf.setFontPointSize(self.parent.font().pointSize() * 2)
            self.setFormat(0, len(text), bf)
        else:
            self.highlightMarkdown(text,0)
#        self.highlightHtml(text)

    def highlightMarkdown(self, text, strt):
        cursor = QTextCursor(self.document())
        bf = cursor.blockFormat()
        self.setFormat(0, len(text), QColor(self.theme['color']))
        #bf.clearBackground()
        #cursor.movePosition(QTextCursor.End)
        #cursor.setBlockFormat(bf)

        #Block quotes can contain all elements so process it first
        self.highlightBlockQuote(text, cursor, bf, strt)

        #If empty line no need to check for below elements just return
        if self.highlightEmptyLine(text, cursor, bf, strt):
            return

        #If horizontal line, look at pevious line to see if its a header, process and return
        if self.highlightHorizontalLine(text, cursor, bf, strt):
            return

        if self.highlightAtxHeader(text, cursor, bf, strt):
            return

        self.highlightList(text, cursor, bf, strt)

        self.highlightLink(text, cursor, bf, strt)

        self.highlightImage(text, cursor, bf, strt)

        self.highlightBeautifiers(text, cursor, bf, strt)

        self.highlightCodeBlock(text, cursor, bf, strt)

    def highlightBlockQuote(self, text, cursor, bf, strt):
        found = False
        mo = re.search(self.MARKDOWN_LINE_KEYS_REGEX['BlockQuote'],text)
        if mo:
            self.setFormat(mo.start(), mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['BlockQuote'])
            unquote = re.sub(self.MARKDOWN_LINE_KEYS_REGEX['BlockQuoteCount'],'',text)
            spcs = re.match(self.MARKDOWN_LINE_KEYS_REGEX['BlockQuoteCount'],text)
            spcslen = 0
            if spcs:
                spcslen = len(spcs.group(0))
            self.highlightMarkdown(unquote,spcslen)
            found = True
        return found

    def highlightEmptyLine(self, text, cursor, bf, strt):
        textAscii = str(text.replace('\u2029','\n'))
        if textAscii.strip():
            return False
        else:
            return True

    def highlightHorizontalLine(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['HR'],text):
            prevBlock = self.currentBlock().previous()
            prevCursor = QTextCursor(prevBlock)
            prev = prevBlock.text()
            prevAscii = str(prev.replace('\u2029','\n'))
            if prevAscii.strip():
                #print "Its a header"
                prevCursor.select(QTextCursor.LineUnderCursor)
                #prevCursor.setCharFormat(self.MARKDOWN_KWS_FORMAT['Header'])
                formatRange = QTextLayout.FormatRange()
                formatRange.format = self.MARKDOWN_KWS_FORMAT['Header']
                formatRange.length = prevCursor.block().length()
                formatRange.start = 0
                prevCursor.block().layout().setAdditionalFormats([formatRange])
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HR'])

        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['eHR'],text):
            prevBlock = self.currentBlock().previous()
            prevCursor = QTextCursor(prevBlock)
            prev = prevBlock.text()
            prevAscii = str(prev.replace('\u2029','\n'))
            if prevAscii.strip():
                #print "Its a header"
                prevCursor.select(QTextCursor.LineUnderCursor)
                #prevCursor.setCharFormat(self.MARKDOWN_KWS_FORMAT['Header'])
                formatRange = QTextLayout.FormatRange()
                formatRange.format = self.MARKDOWN_KWS_FORMAT['Header']
                formatRange.length = prevCursor.block().length()
                formatRange.start = 0
                prevCursor.block().layout().setAdditionalFormats([formatRange])
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HR'])
        return found

    def highlightAtxHeader(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['HeaderAtx'],text):
            #bf.setBackground(QBrush(QColor(7,54,65)))
            #cursor.movePosition(QTextCursor.End)
            #cursor.mergeBlockFormat(bf)
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HeaderAtx'])
            found = True
        return found

    def highlightList(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['UnorderedList'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start()-strt, self.MARKDOWN_KWS_FORMAT['UnorderedList'])
            found = True

        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['OrderedList'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start()-strt, self.MARKDOWN_KWS_FORMAT['OrderedList'])
            found = True
        return found

    def highlightLink(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_INLINE_KEYS_REGEX['Link'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start()-strt, self.MARKDOWN_KWS_FORMAT['Link'])
            found = True
        return found

    def highlightImage(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_INLINE_KEYS_REGEX['Image'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start()-strt, self.MARKDOWN_KWS_FORMAT['Image'])
            found = True
        return found


    def highlightBeautifiers(self, text, cursor, bf, strt):
        found = False
        for t in self.MARKDOWN_INLINE_BEAUTIFIERS:
            for mo in re.finditer(self.MARKDOWN_INLINE_KEYS_REGEX[t],text):
                # Delimiter        
                self.setFormat(mo.start("delim")+strt,
                               len(mo.group("delim")),
                               self.MARKDOWN_KWS_FORMAT["Delim"])
                # Text                
                self.setFormat(mo.start("text") + strt, 
                               len(mo.group("text")) - strt, 
                               self.MARKDOWN_KWS_FORMAT[t])
                # Delimiter
                self.setFormat(mo.start("text") + len(mo.group("text")) +strt,
                               len(mo.group("delim")), 
                               self.MARKDOWN_KWS_FORMAT["Delim"])
                found = True

        return found

    def highlightCodeBlock(self, text, cursor, bf, strt):
        found = False
        for mo in re.finditer(self.MARKDOWN_LINE_KEYS_REGEX['CodeBlock'],text):
            stripped = text.lstrip()
            if stripped[0] not in ('*','-','+','>'):
                self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['CodeBlock'])
                found = True
        return found

    def highlightHtml(self, text):
        for mo in re.finditer(self.MARKDOWN_INLINE_KEYS_REGEX['Html'], text):
            self.setFormat(mo.start(), mo.end() - mo.start(), self.MARKDOWN_KWS_FORMAT['HTML'])
