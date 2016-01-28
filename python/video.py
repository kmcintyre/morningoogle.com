from twisted.python import log

import subprocess

def launch_avi_mp3(video, audio, combined):
    args = ['avconv', '-i', video, '-i', audio, '-y', '-map', '0', '-map', '1', '-codec', 'copy', combined]
    log.msg('launch_avi_mp3:', args)    
    return subprocess.check_call(args)

def launch_avi_ogv(avi, ogv):
    args = ['avconv', '-i', avi, '-acodec', 'libvorbis', '-f', 'ogg', ogv]
    log.msg('launch_avi_ogv:', args)
    return subprocess.check_call(args)

def launch_avi_mp4(avi, mp4):
    args = ['avconv', '-i', avi, '-c:v', 'libx264', mp4]
    log.msg('launch_avi_mp4:', args)
    return subprocess.check_call(args)

def launch_mp4_preview(mp4):
    args = ['avconv', '-i', mp4, '-r', '.1', '-f', 'image2', '%04d.png']
    log.msg('launch_mp4_preview:', args)
    return subprocess.check_call(args)

def launch_preview_gif(mp4_gif):
    args = ['convert', '-delay', '50', '-loop', '1', '*.png', mp4_gif]
    log.msg('launch_preview_gif:', args)
    return subprocess.check_call(args)