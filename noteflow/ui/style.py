#!/usr/bin/env python
# --!-- coding: utf8 --!--


# default window color (linux):
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import qApp

# window = "#d6d2d0" #"#eee" / #eff0f1
window = qApp.palette().color(QPalette.Window).name()

bgHover = "#ccc"
bgChecked = "#bbb"
borderColor = "darkGray"
blue = "#268bd2"


def mainWindowSS():
    return """
            QScrollBar{background:transparent;}
            QScrollBar:handle{
                background:rgba(0, 0, 0, 32);
                border-radius:2px;}
            QScrollBar:vertical{width: 6px;}
            QScrollBar:horizontal{width: 6px;}
            QScrollBar:add-line{background:none;border:none;}
            QScrollBar:sub-line{background:none;border:none;}

            QGroupBox{border:none; margin: 2ex 0 0 2ex; font-weight: bold;}
            QGroupBox:title{subcontrol-origin: margin;}

            QStatusBar::item {border: 0px;}
            """

def webViewSS():
    return "QWebView{{background:{}; }}".format(window)

def tableSS():
    return "background:transparent;"

def lineEditSS_2():
    # return "border-radius: 6px;"
    return """QLineEdit{{
        border: none;
        border-bottom: 1px solid {checked};
        background:transparent;
    }}
    QLineEdit:hover{{
        border-bottom: 1px solid {hover};
    }}
    QLineEdit:focus{{
        border-bottom: 1px solid blue;
    }}
    """.format(window=window,
               checked=bgChecked,
               hover=borderColor,
               blue=blue)


def transparentSS():
    return """background: transparent;
              border:none;"""

def tabBarSS():
    return """
        QTabWidget::pane{{
            margin-top: -1px;
            border: 1px solid #999;
        }}
        QTabWidget::tab-bar{{
            left:50px;
        }}
        QTabBar{{
            background: transparent;
            border-radius: 0;
            border: 0px;
        }}
        QTabBar::tab{{
            margin: 5px 0 0px 0;
            padding: 2px 9px;
            border: 1px solid #999;
            border-bottom: 0px;
        }}
        QTabBar::tab::first{{
            font-weight: bold;
        }}
        QTabBar::tab:selected{{
            border: 1px solid black;
            background: white;
            border-bottom: 0px;
            margin-top: 0px;
            color: black;
        }}
        QTabBar::tab:!selected:hover{{
            background:#ddd;
        }}
        """.format()

def textEditorSS():
    return """
        QTextEdit {{
            border: 0px;
        }}
        QTextEdit:disabled {{
            background: transparent;
        }}

    """.format()
