from PyQt5.QtCore import QUrl, QSize, Qt, QPoint
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtGui import QImage, QPainter

import fixed

from twisted.internet import reactor, defer
from twisted.python import log
            
class SimpleQWebPage(QWebPage):

    disconnect_timeout = 60
    natural_delay_response = 2

    browser_tmp_dir = fixed.tmp_disk

    def __init__(self, *args, **kwargs):
        super(SimpleQWebPage, self).__init__(*args, **kwargs)
        log.msg('new simple web page')
        self.loadFinished.connect(self._page_finished)

        self.setView(QWebView())
        self.view().resize(QSize(1024, 768))

        self.view().setPage(self)
        self.settings().setAttribute(QWebSettings.AutoLoadImages, True)
        self.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebSettings.JavaEnabled, False)
        self.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
        self.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebSettings.NotificationsEnabled, False)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.page_finished_deferred = []

    def _page_finished(self, ok):
        for d in self.page_finished_deferred:
            if not d.called:
                d.callback(ok)
                return
    def page_deferred(self, gather):
        # print 'all cookies:', self.networkAccessManager().cookieJar()
        def cancel_timeout_and_forward(reply, timer):
            # print 'reply:', reply, 'loader:', self.loader
            if not timer.called:
                timer.cancel()
            dr = defer.Deferred()
            dr.addCallback(defer.succeed)
            reactor.callLater(self.natural_delay_response, dr.callback, reply)
            return dr

        def timeout(timed_deferred):
            log.msg('TIMEOUT:', gather['URI'], self.view().url().toString(), self.loader[
                    'percentage'], self.disconnect_timeout)
            if not timed_deferred.called:
                log.msg('cancel request', self.loader[
                        'percentage'], 'stop?:', self.stop_on_error)
                if self.stop_on_error:
                    reactor.stop()

        def page_error(err):
            log.msg('page error', err, gather['URI'], 'stop?:', self.stop_on_error)
            if self.stop_on_error:
                reactor.stop()
        if 'skip' in gather:
            for x in range(gather['skip']):
                log.msg('add skip:', x, 'of:', gather['skip'])
                self.page_finished_deferred.append(
                    defer.Deferred().addCallback(lambda res: log.msg(res)))
        d = defer.Deferred()
        timer = reactor.callLater(self.disconnect_timeout, timeout, d)
        d.addCallback(cancel_timeout_and_forward, timer)
        d.addErrback(page_error)

        self.page_finished_deferred.append(d)
        self.view().load(QUrl(gather['URI']))
        return d