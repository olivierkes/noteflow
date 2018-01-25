#!/usr/bin/env python
#--!-- coding: utf8 --!--

import os, re, json, string

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *


def appPath(suffix=None):
    p = os.path.realpath(os.path.join(os.path.split(__file__)[0], ".."))
    if suffix:
        p = os.path.join(p, suffix)
    return p

def loadJSON(path):
    with open(appPath(path)) as f:
        return json.load(f)

def countWords(words):
    r = {}
    for w in words:
        if w in r:
            r[w] += 1
        else:
            r[w] = 1
    return r

def settings(key=None, default=None, type=None):
    #~/.config/noteflow/noteflow.conf on my systems
    s = QSettings(qApp.organizationName(), qApp.applicationName())
    if key is None:
        return s
    else:
        if type:
            return type(s.value(key, default))
        else:
            return s.value(key, default)

def countDicts(dicts):
    r = {}
    for d in dicts:
        for w in d:
            if w in r:
                r[w] += d[w]
            else:
                r[w] = d[w]
    return r

UID = 0
def uniqueID():
    global UID
    UID += 1
    return UID

def findRowByUserData(table, data):
    "Search in a table userData"
    matches = table.model().match(table.model().index(0,0), Qt.UserRole, data,
                                  flags = Qt.MatchExactly)
    if matches:
        return table.item(matches[0].row(), matches[0].column())

def findNoteByUID(notebooks, UID):
    for nb in notebooks:
        for n in nb.notes:
            if n.UID == UID:
                return n
    return None

def slugify(name):
    """
    A basic slug function, that escapes all spaces to "_" and all non letters/digits to "-".
    @param name: name to slugify (str)
    @return: str
    """
    valid = string.ascii_letters + string.digits
    newName = ""
    for c in name:
        if c in valid:
            newName += c
        elif c in string.whitespace:
            newName += "_"
        else:
            newName += "-"
    return newName

def loadTextFile(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()

def strToDate(date):
    return QDate(*[int(i) for i in date.split("-")])

def stats(text):
    w = len(re.findall(r"\b[\w'-]+\b", text))
    text = text.replace("\n", "")
    c = len(text)
    c2 = len([c for c in text if c.strip()])

    return w, c, c2

def openURL(url):
    """
    Opens url (string) in browser using desktop default application.
    """
    QDesktopServices.openUrl(QUrl(url))

nm = QNetworkAccessManager()
getImageCache = {}
requestSettings = {}

def getImage(url, callback, savedVars=None):
    global getImageCache, requestSettings
    url = QUrl(url)
    if url in getImageCache:
        if getImageCache[url] is not None:
            return callback(*getImageCache[url], savedVars)
        else:
            return

    getImageCache[url] = None
    requestSettings[url] = (callback, savedVars)
    request = QNetworkRequest(url)
    nm.get(request)

def nmFinished(reply):
    global getImageCache, requestSettings
    url = reply.url()
    nmCallback, nmSavedVars = requestSettings[url]
    if reply.error() != QNetworkReply.NoError:
        getImageCache[url] = (False, reply.errorString())
        print(reply.errorString())
        nmCallback(False, reply.errorString(), nmSavedVars)
    else:
        px = QPixmap()
        px.loadFromData(reply.readAll())
        px = px.scaled(800, 600, Qt.KeepAspectRatio)
        getImageCache[url] = (True, px)
        nmCallback(True, px, nmSavedVars)
nm.finished.connect(nmFinished)

def pixmapToTooltip(pixmap):
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG", quality=100)
    image = bytes(buffer.data().toBase64()).decode()
    return "<p><img src='data:image/png;base64,{}'></p>".format(image)

def linkMatchedNote(title, url):
    from noteflow import MW
    allNotes = MW.allNotes()

    if url[:4] == "n://":
        date = url[4:14]
        title = url[15:]
        search = [n for n in allNotes
                  if n.date == date
                  and n.title == title]
        if search:
            n = search[0]
            return n

    # [title](date) → date, and title in note's title
    search = [n for n in allNotes
              if title.lower() in n.title.lower()
              and n.date == url]
    if search:
        n = search[0]
        return n

    # [](2017-12-18/Title) → 2018-12-18/Something with Title in it
    search = [n for n in allNotes
              if n.date in url
              and "/" in url
              and url.split("/")[1] != ""
              and url.split("/")[1].lower() in n.title.lower()]
    if search:
        n = search[0]
        return n

    # [](Title) → first note whose title starts with "Title"
    search = [n for n in allNotes
              if url.lower() == n.title[:len(url)].lower()]
    if search:
        n = search[0]
        return n

def fixLocalLinks(text):

    def repl(m):
        if len(m.groups()) == 2:  # automatic link
            title = m.groups()[0]
            url = m.groups()[1]

        else:
            title = m.group(1)
            url = m.group(2)
        n = linkMatchedNote(title, url)
        if n:
            txt = "[{title}](n://{date}/{title})".format(title=n.title,
                                                         date=n.date)
            return txt
        else:
            return(m.group(0))

    for rx in [
            re.compile(r"(?!!)\[([^\n]+?)\]\(([^\n]+?)\)"),
            re.compile(r"(<([a-zA-Z]+\:[^\n]+?)>)")
        ]:
        text = rx.sub(repl, text)

    return text
