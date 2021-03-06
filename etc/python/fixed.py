import time
import datetime

FRAME_SIZE = 2 ** 20 * 4

import os

tmp_disk = '/tmp/'

def simpleurl(url):
    from urlparse import urlparse
    if not urlparse(url).scheme:
        return "http://" + url
    return url

def environment():
    from os.path import expanduser
    env_vars = {"PYTHONPATH": expanduser('~') + '/scewpt/'}
    env_vars['LIBOVERLAY_SCROLLBAR'] = '0'
    if "DISPLAY" in os.environ:
        env_vars["DISPLAY"] = os.environ["DISPLAY"]
    else:
        env_vars["DISPLAY"] = ":0"
    return env_vars

def yesterday():
    return str(datetime.datetime.fromtimestamp(time.mktime(time.gmtime())-24*60*60)).split(' ')[0] 

def gmt_string():
    return str(datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))).split(' ')[0]

ds_format = '%Y_%m_%d'
dt_format = ds_format + '/%H_%M_%S'
dt_single_format = '%Y_%m_%d_%H_%M_%S'

NO_SUBJECT = "(no subject)"