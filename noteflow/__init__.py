# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWebEngineWidgets

_version = "0.1.0"

import noteflow.functions as F

MW = None


def run():
    global MW

    app = QApplication(sys.argv + ["--disable-web-security"])
    app.setOrganizationName("noteflow")
    app.setOrganizationDomain("www.theologeek.ch")
    app.setApplicationName("noteflow")
    app.setApplicationVersion(_version)

    #icon = QIcon()
    #for i in [16, 31, 64, 128, 256, 512]:
        #icon.addFile(appPath("icons/noteflow/icon-{}px.png".format(i)))
    #qApp.setWindowIcon(icon)

    #app.setStyle("fusion")
#
#    # Load style from QSettings
    settings = F.settings()
#    if settings.contains("applicationStyle"):
#        style = settings.value("applicationStyle")
#        app.setStyle(style)

    # Translation process
    locale = QLocale.system().name()

    appTranslator = QTranslator()
    # By default: locale
    translation = F.appPath(os.path.join("i18n", "noteflow_{}.qm".format(locale)))

    # Load translation from settings
    if settings.contains("applicationTranslation"):
        translation = F.appPath(os.path.join("i18n", settings.value("applicationTranslation")))
        print("Found translation in settings:", translation)

    if appTranslator.load(translation):
        app.installTranslator(appTranslator)
        print(app.tr("Loaded translation: {}.").format(translation))

    else:
        pass
        # qDebug(app.tr("Warning: failed to load translator for locale {}...").format(locale))

#    print(QIcon.themeSearchPaths())
    # QIcon.setThemeSearchPaths(QIcon.themeSearchPaths() + [F.appPath("icons")])
    # QIcon.setThemeName("Mint-X")
    # qApp.setWindowIcon(QIcon.fromTheme("im-aim"))

    # Seperating launch to avoid segfault, so it seem.
    # Cf. http://stackoverflow.com/questions/12433491/is-this-pyqt-4-python-bug-or-wrongly-behaving-code
    launch()


def launch():
    global MW

    from .mainWindow import MainWindow
    MW = MainWindow()
    MW.show()

    qApp.exec_()
#    qApp.deleteLater()
