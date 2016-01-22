print 'going QT'
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication
import os
import boto
os.environ['LIBOVERLAY_SCROLLBAR'] = '0'
boto.config.get('ec2', 'use-sigv4', True)
#if os.environ.get('QTDISPLAY'):
#    os.putenv('DISPLAY', ':' + os.environ.get('QTDISPLAY'))
#else:
os.putenv('DISPLAY', ':0')
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '1234'
from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize
import cv2
qt_version = QtCore.qVersion()


class App(QApplication):

    painter = QPainter()
    events = []
    ready = False
    video = None
    video_frames_per_second = 10
    overwrite = True

    def isReady(self, reply):
        print 'READY!:', reply
        App.ready = reply
        print 'video (env)', os.getenv('VIDEO')
        App.video = cv2.VideoWriter(os.getenv('VIDEO'), cv2.cv.CV_FOURCC(
            'M', 'J', 'P', 'G'), self.video_frames_per_second, (1024, 768), True)

    def done_video(self):
        print 'done video:'
        cv2.destroyAllWindows()
        print 'cv2 destroyed'
        self.video.release()
        print 'video released'

    def notify(self, receiver, event):
        if isinstance(event, QKeyEvent):
            pass
        if isinstance(event, QMouseEvent) and event.type() in [2, 3]:
            print event.pos().x(), event.pos().y(), event.type()
            pass
        if isinstance(receiver, QWebView):
            if self.ready and self.painter and not self.painter.isActive():
                try:
                    image = QImage(QSize(1024, 768), QImage.Format_RGB32)
                    App.painter.begin(image)
                    App.painter.setRenderHint(QPainter.Antialiasing, True)
                    App.painter.setRenderHint(QPainter.TextAntialiasing, True)
                    App.painter.setRenderHint(
                        QPainter.SmoothPixmapTransform, True)
                    App.painter.setRenderHint(
                        QPainter.HighQualityAntialiasing, True)
                    receiver.page().mainFrame().render(App.painter)
                    # print 'write:', self.painter, App.video
                    image.save("temp.jpg", "jpg")
                    App.video.write(cv2.imread('temp.jpg'))
                    App.painter.end()
                except Exception as e:
                    print 'notify ready fail:', e
            else:
                pass
            # print 'busy'

        return super(App, self).notify(receiver, event)
app = App([])
print 'created app'
import qt5reactor
print 'install qt5reactor'
qt5reactor.install()


def closingDown(int1, int2, int3=None):
    print 'closingDown int1:', int1, 'int2:', int2, 'int3:', int3
    if app.ready:
        print 'stop video...'
        app.done_video()
    app.closeAllWindows()
    if not int3:
        from twisted.internet import reactor
        print 'call stop'
        reactor.callLater(0, reactor.stop)


def signalDown(int1, int2, int3=None):
    print 'signal down! calling app quit'
    app.quit()
    closingDown(int1, int2, int3)
import signal
signal.signal(signal.SIGINT, signalDown)
