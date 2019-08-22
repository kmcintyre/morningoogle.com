from PyQt5 import QtWebEngineWidgets 
print 'going QT-force load of QtWebEngineWidgets:', QtWebEngineWidgets

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QOpenGLWidget 
from PyQt5.QtGui import QPaintEvent
import os
import boto

if os.environ.get('QTDISPLAY'):
    print '    DISPLAY=', os.environ.get('QTDISPLAY')
    os.putenv('DISPLAY', os.environ.get('QTDISPLAY'))
else:
    print 'DISPLAY :0'
    os.putenv('DISPLAY', ':0')
boto.config.get('ec2', 'use-sigv4', True)
from PyQt5 import QtCore
import cv2
qt_version = QtCore.qVersion()

def filesubpath(filename):
    try:
        os.makedirs(os.path.dirname(filename))
    except:
        pass
    
class App(QApplication):

    def initCapture(self):
        self.capture = True   
        self.opengl = None
        self.video = None
        self.location = '/home/ubuntu/Desktop/capture.avi'
        self.jpg_location = '/tmp/capture.jpg'
        
    def frame(self):  
        if self.video and self.opengl:               
            self.opengl.grabFramebuffer().save( self.jpg_location, 'JPG')
            try:                 
                self.video.write( cv2.imread(self.jpg_location) )
            except Exception as e:
                print '    OH no!', e
    
    def stopVideo(self):
        app.timer.stop()
        app.video.release()
        
    def toVideo(self, fps=10, location = None, jpg_location = None):
        if location:
            filesubpath(location)
            self.location = location
        if jpg_location:
            filesubpath(jpg_location)        
            self.jpg_location = jpg_location
        print 'VIDEO CAPTURE', self.location, 'via:', self.jpg_location, 'at:', fps        
        timer = QTimer()
        timer.timeout.connect(self.frame)
        self.timer = timer        
        self.video = cv2.VideoWriter(self.location,  cv2.cv.CV_FOURCC('M','J','P','G'), fps, (1024,768), True)
        print 'is open:', self.video.isOpened()
        self.timer.start(1000/fps)
        
     
    def toImage(self, location = None):
        if not self.opengl:
            print 'location:', location, 'not captured'
            return        
        png = '/tmp/capture.png'
        if location:
            png = location 
        filesubpath(png)
        print 'IMAGE CAPTURE', png
        self.opengl.grabFramebuffer().save( png, 'PNG')        

    def notify(self, receiver, event):
        if self.capture and isinstance(receiver, QOpenGLWidget):
            self.opengl = receiver                      
        return super(App, self).notify(receiver, event)

app = App([])
app.initCapture()
#app.enabled = True

print 'created app'
import qt5reactor
print 'install qt5reactor'
qt5reactor.install()
from twisted.internet import reactor

def signalDown(int1, int2, int3=None):
    if app.video and app.video.isOpened():
        print 'stop video:', app.video
        app.stopVideo()
        print 'is open:', app.video.isOpened()
        cv2.destroyAllWindows()          
    print 'signal down! calling app quit'
    app.closeAllWindows()
    print 'next'  
    reactor.stop()    
    print 'last'
    return 0
import signal
signal.signal(signal.SIGINT, signalDown)