import qt5
print 'window:', qt5.qt_version

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWebEngineWidgets
from twisted.web.xmlrpc import XMLRPC
from PyQt5.QtCore import QUrl, QSize, Qt, QPoint
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtTest import QTest

from twisted.python import log

import fixed

from page import SimpleQWebPage
from twisted.internet import defer

class Window(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.web_page = SimpleQWebPage()
        log.msg('scewpt window init')
        self.resize(QSize(1024, 768))
        self.setCentralWidget(self.web_page.view())

    def xmlrpc_goto_url(self, url, skip=None):
        print 'goto:', url
        url = fixed.simpleurl(url)
        #log.msg('goto:', url, 'from:', self.web_page.view().url().toString())
        gather = {'URI': url}
        if skip:
            log.msg('set skip:', skip)
            gather.update({'skip': skip})
        d = self.web_page.page_deferred(gather)
        return d

    def xmlrpc_click(self, x, y, delay_secs=1):
        # log.msg('click:', x, 'x', y
        QTest.mouseClick(
            self.web_page.view(), Qt.LeftButton, Qt.NoModifier, QPoint(x, y))
        return self.xmlrpc_delay(True, delay_secs)

    def xmlrpc_scroll_to_bottom(self, bottom_limit=None):
        log.msg('scroll to bottom')

        def at_bottom():
            ab = not self.web_page.mainFrame().scrollBarMaximum(Qt.Vertical) > self.web_page.mainFrame().scrollBarValue(
                Qt.Vertical) or (bottom_limit and self.web_page.mainFrame().scrollBarValue(Qt.Vertical) > bottom_limit)
            if ab:
                log.msg(
                    'At Bottom:', self.web_page.mainFrame().scrollBarMaximum(Qt.Vertical))
            return ab
        while not at_bottom():
            log.msg('moving to bottom')
            QTest.qWait(200)
            QTest.keyClick(
                self.web_page.view(), Qt.Key_PageDown, Qt.NoModifier, 50)
        return defer.succeed(self.web_page.mainFrame().scrollBarMaximum(Qt.Vertical))

    '''
    must investigate
    '''

    def xmlrpc_flash_set(self, setting=True):
        self.web_page.settings().setAttribute(
            QWebSettings.PluginsEnabled, setting)
        return self.web_page.page_deferred(gather={'URI': 'http://www.adobe.com/software/flash/about/'})

    def xmlrpc_google_suggest(self, url='https://www.google.com/', q='', delay=2):
        gather = {}
        gather['URI'] = '{0}?q={1}'.format(url, q)

        def hitdown(res):
            QTest.keyClick(self.web_page.view(), Qt.Key_Down, Qt.NoModifier, 50)
            if url == 'https://www.google.com/':
                QTest.qWait(delay * 3000)
            else:
                QTest.qWait(delay * 1000)
            QTest.keyClick(
                self.web_page.view(), Qt.Key_Escape, Qt.NoModifier, 50)
            return defer.SUCCESS
        d = self.web_page.page_deferred(gather)
        d.addCallback(hitdown)
        return d