import fixed

from twisted.python.filepath import FilePath
from twisted.web.template import renderer, XMLFile, tags

from twisted.web.template import Element

import time

from twisted.python import log


class MorningElement(Element):
    loader = XMLFile(FilePath('templates/mg_template.xml'))

    def __init__(self, startrunat, song_credits, mp3_href, mp3_queue):
        self._startrunat = startrunat
        self._song_credits = song_credits
        self._mp3_href = mp3_href
        self._mp3_queue = mp3_queue

    @renderer
    def mp3_link(self, request, tag):
        return tag(tags.a(self._mp3_href[52:], href=self._mp3_href))
        # return tag(str(self._mp3_href))

    @renderer
    def song_credits(self, request, tag):
        return tag(str(self._song_credits))

    @renderer
    def queue(self, request, tag):
        for m in self._mp3_queue:
            yield tag.clone().fillSlots(song=m.key[30:])

    @renderer
    def startrunas(self, request, tag):
        return tag(str(self._startrunat))


def create_morning_element(js, mp3, mp3_queue):
    log.msg('create_morning_element:', js, mp3_queue)
    sc = fixed.NO_SUBJECT
    try:
        log.msg('subject:')
        sc = js['subject']
    except Exception as e:
        log.msg('exception with subject:', e)
    return MorningElement(startrunat=time.time(), song_credits=sc, mp3_href='http://www.scewpt.com/' + mp3.key, mp3_queue=mp3_queue)
