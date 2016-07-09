import qt5
print 'morning:', qt5.qt_version


from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineSettings
import fixed
import video

import subprocess

import sys
import os

from twisted.python import log
import boto3

mg_date = fixed.gmt_string()
mg_snd = 'today_sound.avi'
mg_mp3 = 'today.mp3'
mg_ogv = mg_date + '.ogv'
mg_mp4 = mg_date + '.mp4'
mg_gif = mg_date + '.gif'

s3 = boto3.resource('s3')
bucket = s3.Bucket('morningoogle.com')
s3_client=boto3.client('s3')


from lxml import html
from twisted.internet import reactor, defer, task
from twisted.web.client import getPage

from window import Window

class Messenger():

    def __init__(self):
        pass

    def message(self, ign=None):
        if ign:
            return "thank you"
        else:
            return "morning"
        
messenger = Messenger()
class WikipediaGoogleDomains():

    def callbackExtractGoogle(self, h):
        google = []
        doc = html.document_fromstring(h)
        n = doc.cssselect('a[title="Ascension Island"]')[0]
        
        google.append(('Worldwide', '.COM', 'https://www.google.com/'))
        for tr in n.getparent().getparent().getparent()[2:]:
            try:
                country_name = tr[0].find("a").text
                iso = tr[1][0][0].text
                domain = tr[2][0][0].get('href')
                #log.msg('domain:', domain)
                google.append((country_name, iso, domain))
                
            except Exception as e:
                log.msg('google domain exception:', e)
        print 'search domains length:', len(google)
        return google

    def google_domains(self):        
        d = getPage('http://en.wikipedia.org/wiki/List_of_Google_domains')
        d.addCallback(self.callbackExtractGoogle)
        return d

@defer.inlineCallbacks
def domain_loop(window):
    for search_domain in window.domains:
        log.msg('search_domain:', search_domain)
        d = window.google_suggest(search_domain[2], messenger.message(None))
        yield d

@defer.inlineCallbacks
def google_news(res, window):
    log.msg('get_google_news', res) 
    d = window.goto_url('https://news.google.com')
    d.addCallback(lambda res: task.deferLater(reactor, 2, defer.succeed, res))
    d.addCallback(lambda res: window.scroll_to_bottom(100))    
    yield d 

@defer.inlineCallbacks
def gmt_date(window):
    d = window.goto_url('https://www.google.com/search?q=gmt+time')
    d.addCallback(lambda res: task.deferLater(reactor, 3, defer.succeed, res))    
    yield d

window = Window()
window.page().profile().setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
window.page().settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)

@defer.inlineCallbacks
def start_mg():
    window.show()
    log.msg('start_mg:', window)
    wgg = WikipediaGoogleDomains()
    window.domains = yield wgg.google_domains()    
    qt5.app.toVideo()
    mp3 = list(bucket.objects.filter(Prefix='audio/' + mg_date[5:]))[0]
    boto3.client('s3').download_file(bucket.name, mp3.key, mg_mp3)
    print 'got mp3'            
    d = gmt_date(window)    
    d.addCallback(google_news, window)
    d.addCallback(lambda ign: domain_loop(window) )
    #yield task.deferLater(reactor, 1, defer.succeed, True)
    yield d
    qt5.app.stopVideo()
    window.close()    
    print 'compress' 
    avi_result = video.launch_avi_mp3(qt5.app.location, mg_mp3, mg_snd)
    print 'avi_result:', avi_result
    ogv_result = video.launch_avi_ogv(mg_snd, mg_ogv)
    print 'ogv_result:', ogv_result    
    mp4_result = video.launch_avi_mp4(mg_snd, mg_mp4)
    print 'mp4_result:', mp4_result    
    preview_result = video.launch_mp4_preview(mg_mp4)
    print 'preview_result:', preview_result
    gif_result = video.launch_preview_gif(mg_gif)
    print 'gif_result:', gif_result
    filelist = [ f for f in os.listdir('.') if f.endswith('.png') ]
    for f in filelist:
        os.remove(f) 
            
    os.remove(mg_snd)
    os.remove(mg_mp3)
        
    subprocess.check_call(['cp', mg_gif, '../public/preview/'])
    s3.Bucket('morningoogle.com').put_object(Key='preview/' + mg_gif, Body=open(mg_gif, 'rb'), ACL='public-read', ContentType='image/gif')
    os.remove(mg_gif)
    
    subprocess.check_call(['cp', mg_mp4, '../public/video/'])
    s3.Bucket('morningoogle.com').put_object(Key='video/' + mg_mp4, Body=open(mg_mp4, 'rb'), ACL='public-read', ContentType='video/mp4')
    os.remove(mg_mp4)
    
    subprocess.check_call(['cp', mg_ogv, '../public/ogv/'])
    s3.Bucket('morningoogle.com').put_object(Key='ogv/' + mg_ogv, Body=open(mg_ogv, 'rb'), ACL='public-read', ContentType='video/ogg')
    os.remove(mg_ogv)
    reactor.stop()

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    window.show()
    reactor.callWhenRunning(start_mg)
    reactor.run()
