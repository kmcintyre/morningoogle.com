import qt5
print 'window:', qt5.qt_version

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

from twisted.internet import defer, reactor, task

class Window(QWebEngineView):
    
    js_common_fmt="""
        //while (document.body.scrollHeight > document.body.scrollTop) {
        //}
        """        
    js_fake_key_fmt="""
        var el = document.activeElement;
        function keyin(keyCode, noup) {
            var event = document.createEvent('KeyboardEvent'); // create a key event
            // define the event
            alert(keyCode + ' ' + noup);            
            event.initKeyEvent(noup?"keydown":"keypress",       // typeArg,                                                           
                   true,             // canBubbleArg,                                                        
                   true,             // cancelableArg,                                                       
                   null,             // viewArg,  Specifies UIEvent.view. This value may be null.     
                   false,            // ctrlKeyArg,                                                               
                   false,            // altKeyArg,                                                        
                   false,            // shiftKeyArg,                                                      
                   false,            // metaKeyArg,                                                       
                    9,               // keyCodeArg,                                                      
                    keyCode);              // charCodeArg);                
            el.dispatchEvent(event);
        }        
        var term = '%s';
        for (var x = 0; x < term.length; x++) {            
            keyin(term.charCodeAt(x), false);            
        }
        //#keyin(40, true);
    """ 
    
    def scroll_to_bottom(self, tick):
        self.page().runJavaScript(self.js_common_fmt)        
    
    def __init__(self):
        print '    BANG'
        super(QWebEngineView, self).__init__()            
        self.deferred_cbs = []
        self.setFixedWidth(1024)
        self.setFixedHeight(768)
        self.page().loadFinished.connect(self.finished)

    def finished(self, ok):
        print 'finished-', len(self.deferred_cbs), self.page().url().toString()
        for deferred in self.deferred_cbs:
            if not deferred.called:
                if not ok:
                    print 'not okay return:', ok
                deferred.callback(ok)
                return
        else:
            print 'no callback'     
        
    def goto_url(self, url):
        print 'goto url:', url, len(self.deferred_cbs)
        qurl = QUrl(url)        
        d = defer.Deferred()
        self.deferred_cbs.append(d)         
        self.page().load(qurl)
        return d
    
    def google_suggest(self, url='http://www.google.com/', q='', delay=2):        
        d = self.goto_url(url)
        #d.addCallback(lambda ign: self.page().runJavaScript(self.js_fake_key_fmt % q))
        d.addCallback(lambda res: task.deferLater(reactor, 1, defer.succeed, res))        
        return d