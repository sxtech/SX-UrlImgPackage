# -*- coding: cp936 -*-
'''This example is a simple WSGI_ script which displays
the ``Hello World!`` message. To run the script type::

    python manage.py

To see all options available type::

    python manage.py -h

.. autofunction:: hello

.. autofunction:: server

.. _WSGI: http://www.python.org/dev/peps/pep-3333/
'''
import os
import json
import time
import urllib
import urlparse
import threading
import Queue
import logging
import logging.handlers

from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB

try:
    from pulsar import MethodNotAllowed
except ImportError:  # pragma nocover
    import sys
    sys.path.append('../../')
    from pulsar import MethodNotAllowed

from pulsar.apps import wsgi
from pulsar.apps import socket 

import gl
from imgdownload import Download
from iniconf import ImgDownloadIni
from sqlitedb import USqlite
from cleaner import Cleaner

def initLogging(logFilename):
    """Init for logging"""
    path = os.path.split(logFilename)
    if os.path.isdir(path[0]):
        pass
    else:
        os.makedirs(path[0])
    logger = logging.getLogger('root')
    
    Rthandler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=100*1024*1024,backupCount=5)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)

def sqliteCustomer():
    sqlite = USqlite()
    sqlite.create_table()     #创建表
    cl = Cleaner(sqlite)      #清除文件类对象
    for i in sqlite.get_users():
        gl.KEYSDICT[i['key']] = {'priority':i['priority'],'power':i['power']}
    #print gl.KEYSDICT
    while 1:
        if not gl.QTFLAG:    #退出检测
            gl.DCFLAG = False
            #print 'out'
            break
        try:
            sq = gl.MYQ.get(block=False)
            data = json.loads(sq)
            if data['op']==3:
                addImg(sqlite,data)
            elif data['op']==7:
                cl.clean_ot_img()
        except Queue.Empty:
            time.sleep(1)
        except Exception,e:
            logger.exception(str(e))
            time.sleep(1)
            
    del sqlite
    del cl

def mainCleaner():
    clCount = 0
    while 1:
        if not gl.QTFLAG:    #退出检测
            gl.DCFLAG = False
            break
        else:
            try:
                if clCount>30:
                    clCount = 0
                    sq = {}
                    sq['op'] = 7
                    gl.MYQ.put(json.dumps(sq))
            except Exception,e:
                logger.error(e)
        clCount += 1
        time.sleep(1)

def addImg(sqlite,data):
    try:
        sqlite.add_imgdownload(data['timestamp'],data['sqlstr'],data['path'])
    except sqlite3.Error as e:
        logger.exception(e)
    
#版本号
def version():
<<<<<<< HEAD
    return 'SX-UrlImgPackage V0.2.1;port:8017;'
=======
    return 'SX-UrlImgPackage V0.1.0'
>>>>>>> parent of ee6c5f7... V0.2.0

def hello(environ, start_response):
    '''The WSGI_ application handler which returns an iterable
    over the "Hello World!" message.'''
    #request_body = environ['wsgi.input']
    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO']== '/urlimgpackage':
        data = request_data(environ["wsgi.input"].read())
        status = '200 OK'
    else:
        data = json.dumps({'package':None,'msg':'Request Error','code':101})
        status = '400 Bad Request'
        
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])

def server(description=None, **kwargs):
    '''Create the :class:`.WSGIServer` running :func:`hello`.'''
    description = description or 'Img Package Application'
    
    return wsgi.WSGIServer(hello, name='UrlImgPackageServer', description=description, **kwargs)

def request_data(wsgi_input):
    data = urllib.unquote_plus(wsgi_input)
    post_data = urlparse.parse_qs(data,True)

    user_info =  gl.KEYSDICT.get(post_data.get('key',[None])[0],None)
    #如果KEY不正确返回错误
    if user_info is None:
        return json.dumps({'package':None,'msg':'Key Error','code':105})
    #JSON格式错误
    if post_data.get('urls',None) == None:
        return json.dumps({'package':None,'msg':'No Urls Parameter','code':110})
    else:
        try:
            url_list = json.loads(post_data.get('urls',[''])[0])
        except Exception as e:
            logger.error(e)
            return json.dumps({'package':None,'msg':'Json Format Error','code':106})
    #print url_list     
    gl.COUNT += 1
    imgd = Download()
    zipfile = imgd.main(url_list)
    del imgd
    
    return json.dumps({'package':zipfile,'msg':'Success','code':100})

class PackageServer:
    def __init__(self):
        self.img = ImgDownloadIni()
        self.sys_ini = self.img.getSysConf()

        gl.BASEPATH = self.sys_ini['path'].replace("/","\\")
        
        gl.MYQ = Queue.Queue()
        t1 = threading.Thread(target=sqliteCustomer, args=())
        t2 = threading.Thread(target=mainCleaner, args=())
        t1.start()
        t2.start()

    def main(self):
        server().start()

if __name__ == '__main__':  # pragma nocover
    initLogging(r'log\imgdownload.log')
    logger = logging.getLogger('root')
        
    ps = PackageServer()
    ps.main()
    del ps
