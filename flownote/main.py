# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import QLocale, QTranslator, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, qApp

_version = "0.1.0"

from flownote.functions import appPath


def run():
    app = QApplication(sys.argv)
    app.setOrganizationName("flownote")
    app.setOrganizationDomain("www.theologeek.ch")
    app.setApplicationName("flownote")
    app.setApplicationVersion(_version)
    
    #icon = QIcon()
    #for i in [16, 31, 64, 128, 256, 512]:
        #icon.addFile(appPath("icons/flownote/icon-{}px.png".format(i)))
    #qApp.setWindowIcon(icon)

    #app.setStyle("fusion")
#
#    # Load style from QSettings
    settings = QSettings(app.organizationName(), app.applicationName())
#    if settings.contains("applicationStyle"):
#        style = settings.value("applicationStyle")
#        app.setStyle(style)

    # Translation process
    locale = QLocale.system().name()

    appTranslator = QTranslator()
    # By default: locale
    translation = appPath(os.path.join("i18n", "flownote_{}.qm".format(locale)))

    # Load translation from settings
    if settings.contains("applicationTranslation"):
        translation = appPath(os.path.join("i18n", settings.value("applicationTranslation")))
        print("Found translation in settings:", translation)

    if appTranslator.load(translation):
        app.installTranslator(appTranslator)
        print(app.tr("Loaded translation: {}.").format(translation))

    else:
        print(app.tr("Warning: failed to load translator for locale {}...").format(locale))

#    print(QIcon.themeSearchPaths())
    QIcon.setThemeSearchPaths(QIcon.themeSearchPaths() + [appPath("icons")])
    QIcon.setThemeName("Mint-X")
    # qApp.setWindowIcon(QIcon.fromTheme("im-aim"))

    # Seperating launch to avoid segfault, so it seem.
    # Cf. http://stackoverflow.com/questions/12433491/is-this-pyqt-4-python-bug-or-wrongly-behaving-code
    launch()


def launch():
    from .mainWindow import MainWindow

    main = MainWindow()
    main.show()

    qApp.exec_()
    qApp.deleteLater()


if __name__ == "__main__":
    run()
