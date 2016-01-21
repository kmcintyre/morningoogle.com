# avconv -i video.avi -i mg.mp3 -map 0 -map 1 -codec copy mg_sound.avi
from twisted.internet import reactor, defer
from twisted.python import log

import fixed

from twisted.runner.procmon import LoggingProtocol


def launch_avi_mp3(video=None, audio=None, combined=None):
    if video and audio and combined:
        args = ['avconv', '-i', video, '-i', audio, '-y',
                '-map', '0', '-map', '1', '-codec', 'copy', combined]
        log.msg('launch_avi_mp3:', args)
        spp = LoggingProtocol()
        return reactor.spawnProcess(spp, args[0], args=args, env=fixed.environment())
    else:
        return defer.FAILURE


def launch_avi_ogv(avi=None, ogv=None):
    if avi and ogv:
        args = ['avconv', '-i', avi, '-acodec', 'libvorbis', '-f', 'ogg', ogv]
        log.msg('launch_avi_ogv:', args)
        spp = LoggingProtocol()
        reactor.spawnProcess(spp, args[0], args=args, env=fixed.environment())
        return spp

    else:
        return defer.FAILURE


def launch_avi_mp4(avi=None, mp4=None):
    log.msg('launch:', avi, 'mp4:', mp4)
    if avi and mp4:
        args = ['avconv', '-i', avi, '-c:v', 'libx264', '-c:a', 'copy', mp4]
        log.msg('launch_avi_mp4:', args)
        spp = LoggingProtocol()
        reactor.spawnProcess(spp, args[0], args=args, env=fixed.environment())
        return spp
    else:
        return defer.FAILURE

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        log.msg('arg1:', sys.argv[1])
    if len(sys.argv) > 2:
        log.msg('arg2:', sys.argv[2])
    if len(sys.argv) > 3:
        log.msg('arg3:', sys.argv[3])
        func = eval('launch_avi_' + sys.argv[2])
        d = func(sys.argv[1], sys.argv[3])
        #d.addCallback(lambda ign: reactor.stop())
    log.msg('starting reactor')
    reactor.run()
'''
avconv -i video.avi -i mg.mp3 -map 0 -map 1 -codec copy mg_sound.avi

avconv -i ms_sound.avi -c:v libx264 -c:a copy $today.mp4
'''
