#!/usr/bin/env python
# --!-- coding: utf8 --!--
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import noteflow.functions as F

features = {'qtwebkit': False, 'qtwebengine': False}

if 'QT_WEB' in os.environ:
    features[os.environ['QT_WEB']] = True
else:
    try:
        import PyQt5.QtWebKitWidgets
        features['qtwebkit'] = True
    except:
        features['qtwebkit'] = False

    try:
        import PyQt5.QtWebEngineWidgets
        features['qtwebengine'] = True
    except:
        features['qtwebengine'] = False

webView = None

if features['qtwebengine']:
    from noteflow.ui.views.webEngineView import webEngineView
    print("Debug: Web rendering engine used: QWebEngineView")
    webEngine = "QtWebEngine"
    webView = webEngineView

elif features['qtwebkit']:
    from PyQt5.QtWebKitWidgets import QWebView
    print("Debug: Web rendering engine used: QWebView (WebKit)")
    webEngine = "QtWebKit"
    webView = QWebView
