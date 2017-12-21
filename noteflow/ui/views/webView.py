#!/usr/bin/env python
# --!-- coding: utf8 --!--
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineCore import *

import noteflow.functions as F

class webView(QWebEngineView):
    def __init__(self, parent=None):
        QWebEngineView.__init__(self, parent)

        self.webPage = webPage(self)
        self.setPage(self.webPage)

class webPage(QWebEnginePage):
    def __init__(self, parent=None):
        QWebEnginePage.__init__(self, parent)

    def acceptNavigationRequest(self, url, navigationType, isMainFrame):
        if navigationType == QWebEnginePage.NavigationTypeLinkClicked:
            n = F.linkMatchedNote("", url.url())
            if n:
                from noteflow import MW
                MW.openNote(n.UID)
                MW.previewNote(True)
            else:
                F.openURL(url)

        return False
