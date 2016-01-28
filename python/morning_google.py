import qt5
print 'morning:', qt5.qt_version

import video_environment
import fixed
import video

import subprocess

import sys
import os

from twisted.python import log
import boto3

mg_date = fixed.gmt_string()
mg_avi = mg_date + '.avi'
mg_ogv = mg_date + '.ogv'
mg_mp4 = mg_date + '.mp4'
mg_gif = mg_date + '.gif'

s3 = boto3.resource('s3')
bucket = s3.Bucket('morningoogle.com')
s3_client=boto3.client('s3')

log.msg('morning!:', mg_avi, mg_ogv)
if not os.path.isfile(mg_avi):
    log.msg('set environment')
    video_environment.set_environment(mg_avi)
else:
    log.msg('video exists:', mg_avi)
    #sys.exit(0)

from lxml import html
from twisted.internet import reactor, defer
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

    '''
    varies
    '''
    # /html/body/div[3]/div[2]/div[4]/table[1]
    # /html/body/div[3]/div[2]/div[4]/table[1]
    # /html/body/div[3]/div[3]/div[4]/table[1]

    def callbackExtractGoogle(self, h):
        google = []
        doc = html.document_fromstring(h)
        n = doc.xpath('/html/body/div[3]/div[3]/div[4]/table[1]')[0]
        google.append(('Worldwide', '.COM', 'https://www.google.com/'))
        for tr in n:
            try:
                country_name = tr[0].find("a").text
                iso = tr[1][0][0].text
                domain = tr[2][0][0].get('href')
                log.msg('domain:', domain)
                google.append((country_name, iso, domain))
            except Exception as e:
                log.msg('google domain exception:', e)
        return google

    def google_domains(self):        
        d = getPage('http://en.wikipedia.org/wiki/List_of_Google_domains')
        d.addCallback(self.callbackExtractGoogle)
        return d

def domain_loop(res, window, loop=0):
    window.web_page.natural_delay_response = .5
    log.msg('domain loop res:', res, 'loop:', loop)
    try:
        search_domain = window.domains[loop]
        log.msg('search_domain:', search_domain)
        d = window.xmlrpc_google_suggest(search_domain[2], messenger.message(None))
        d.addCallback(domain_loop, window, loop + 1)
        return d
    except Exception as e:
        log.msg('exception done?:', e)
        return reactor.stop()

@defer.inlineCallbacks
def google_news(res, window):
    log.msg('get_google_news', res)
    gather = {}
    gather['URI'] = 'https://news.google.com'
    yield window.web_page.page_deferred(gather)
    window.xmlrpc_scroll_to_bottom()

def gmt_date(res, window):
    log.msg('gmtdate', res)
    gather = {}
    gather['URI'] = 'https://www.google.com/search?q=gmt+time'
    d = window.web_page.page_deferred(gather)
    return d

@defer.inlineCallbacks
def start_mg(window):
    window.show()
    log.msg('start_mg:', window)
    wgg = WikipediaGoogleDomains()
    google = yield wgg.google_domains()    
    qt5.app.isReady(True)        
    d = gmt_date(window)
    d.addCallback(google_news, window)
    d.addCallback(domain_loop, window)
    yield d
    window.close()
    print 'compress' 
    if not os.path.isfile('today.mp3'):
        print 'get mp3'
        mp3 = list(bucket.objects.filter(Prefix='audio/' + mg_date[5:]))[0]
        boto3.client('s3').download_file(bucket.name, mp3.key, 'today.mp3')
    avi_result = video.launch_avi_mp3(mg_avi, 'today.mp3', 'today_sound.avi')
    print 'avi_result:', avi_result
    os.remove(mg_avi)
    os.remove('today.mp3')
    ogv_result = video.launch_avi_ogv('today_sound.avi', mg_ogv)
    print 'ogv_result:', ogv_result    
    mp4_result = video.launch_avi_mp4('today_sound.avi', mg_mp4)
    print 'mp4_result:', mp4_result
    os.remove('today_sound.avi')
    preview_result = video.launch_mp4_preview(mg_mp4)
    print 'preview_result:', preview_result
    gif_result = video.launch_preview_gif(mg_gif)
    print 'gif_result:', gif_result
    filelist = [ f for f in os.listdir('.') if f.endswith('.png') ]
    for f in filelist:
        os.remove(f) 
        
    subprocess.check_call(['cp', mg_gif, '../public/preview/'])
    s3.Bucket('morningoogle.com').put_object(Key='preview/' + mg_gif, Body=open(mg_gif, 'rb'), ACL='public-read', ContentType='image/gif')
    os.remove(mg_gif)
    
    subprocess.check_call(['cp', mg_mp4, '../public/video/'])
    s3.Bucket('morningoogle.com').put_object(Key='video/' + mg_mp4, Body=open(mg_mp4, 'rb'), ACL='public-read', ContentType='video/mp4')
    os.remove(mg_mp4)
    
    subprocess.check_call(['cp', mg_ogv, '../public/ogv/'])
    s3.Bucket('morningoogle.com').put_object(Key='ogv/' + mg_ogv, Body=open(mg_ogv, 'rb'), ACL='public-read', ContentType='video/ogg')
    os.remove(mg_ogv)
    

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    window = Window()
    window.show()
    reactor.callLater(1, start_mg, window)
    reactor.run()
