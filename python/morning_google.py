import qt5
print 'morning:', qt5.qt_version

import video_environment
import fixed
import video
import transcoder

import sys
import os

from twisted.python import log
import boto3

mg_date = fixed.gmt_string()
mg_avi = mg_date + '.avi'
mg_ogv = mg_date + '.ogv'
s3 = boto3.resource('s3')
bucket = s3.Bucket('morningoogle.com')

log.msg('morning!:', mg_avi, mg_ogv)
if not os.path.isfile(mg_avi):
    log.msg('set environment')
    video_environment.set_environment(mg_avi)
else:
    log.msg('video exists:', mg_avi)
    sys.exit(0)

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

def ogv():
    process = video.launch_avi_ogv('today_sound.avi', mg_ogv)
    d = defer.Deferred()

    def processEnded():
        log.msg('ogv done!')
        #os.remove('today_sound.avi')
        return d.callback(True)
    process.processEnded = lambda ign: processEnded()
    return d

def compress():
    print 'compress' 
    if not os.path.isfile('today.mp3'):
        mp3 = list(bucket.objects.filter(Prefix='audio/' + mg_date[5:]))[0]
        boto3.client('s3').download_file(bucket.name, mp3.key, 'today.mp3')
    process = video.launch_avi_mp3(mg_avi, 'today.mp3', 'today_sound.avi')
    print 'process:', process
    d = defer.Deferred()
    def processEnded():
        #os.remove('today_2016-01-21.avi')
        log.msg('compress with audio done!')
        return d.callback(True)
    process.processEnded = lambda ign: processEnded()
    return d


def domain_loop(res, window, loop=0):
    window.web_page.natural_delay_response = .5
    log.msg('domain loop res:', res, 'loop:', loop)
    try:
        search_domain = window.domains[loop]
        log.msg('search_domain:', search_domain)
        d = window.xmlrpc_google_suggest(
            search_domain[2], messenger.message(None))
        d.addCallback(domain_loop, window, loop + 1)
        return d
    except Exception as e:
        log.msg('exception done?:', e)
        return reactor.stop()

def google_news(res, window):
    log.msg('get_google_news', res)
    gather = {}
    gather['URI'] = 'https://news.google.com'
    d = window.web_page.page_deferred(gather)
    d.addCallback(window.xmlrpc_scroll_to_bottom)
    return d


def gmt_date(res, window):
    log.msg('gmtdate', res)
    gather = {}
    gather['URI'] = 'https://www.google.com/search?q=gmt+time'
    return window.web_page.page_deferred(gather)

def mg(domains, window):
    log.msg('mg:', len(domains))
    gather = {}
    gather['URI'] = 'http://morningoogle.com'
    window.domains = domains
    return window.web_page.page_deferred(gather)

@defer.inlineCallbacks
def start_mg(window):
    log.msg('start_mg:', window)
    window.show()
    qt5.app.isReady(True)
    wgg = WikipediaGoogleDomains()
    d = wgg.google_domains()
    d.addCallback(mg, window)
    d.addCallback(gmt_date, window)
    d.addCallback(google_news, window)
    d.addCallback(domain_loop, window)
    yield d
    window.close()
    yield compress()
    yield ogv()
    data = open(mg_ogv, 'rb')
    bucket.put_object(Key='ogv/' + mg_ogv, Body=data)
    print transcoder.toMp4('ogv/' + mg_ogv, mg_date)
    
if __name__ == '__main__':
    log.startLogging(sys.stdout)
    window = Window()
    window.show()
    reactor.callLater(2, start_mg, window)
    reactor.run()
