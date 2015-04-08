# -*- coding: utf-8 -*-
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

try:
    from pulsar import MethodNotAllowed
except ImportError:  # pragma nocover
    import sys
    sys.path.append('../../')
    from pulsar import MethodNotAllowed

from pulsar.apps import wsgi
import MySQLdb
from DBUtils.PooledDB import PooledDB

import gl
from imgdownload import Download
from iniconf import ImgDownloadIni
from sqlitedb import USqlite
from mysqldb import UMysql
from cleaner import Cleaner


def init_logging(log_file_name):
    """Init for logging"""
    path = os.path.split(log_file_name)
    if os.path.isdir(path[0]):
        pass
    else:
        os.makedirs(path[0])
    logger = logging.getLogger('root')

    rthandler = logging.handlers.RotatingFileHandler(
        log_file_name, maxBytes=100 * 1024 * 1024, backupCount=5)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s[line:%(lineno)d] \
        [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    rthandler.setFormatter(formatter)
    logger.addHandler(rthandler)


def mysql_pool(h, u, ps, pt, minc=5, maxc=20, maxs=10, maxcon=100, maxu=1000):
    """mysql线程池"""
    gl.MYSQLPOOL = PooledDB(
        MySQLdb,
        host=h,
        user=u,
        passwd=ps,
        db="img_url",
        charset="utf8",
        mincached=minc,
        maxcached=maxc,
        maxshared=maxs,
        maxconnections=maxcon,
        maxusage=maxu)


def sqlite_customer():
    """sqlite数据库操作执行线程"""
    # 创建sqlite对象
    sqlite = USqlite()
    # 创建数据库表
    sqlite.create_table()
    # 清除文件类对象
    cl = Cleaner(sqlite)
    for i in sqlite.get_users():
        gl.KEYSDICT[i['key']] = {
            'priority': i['priority'], 'power': i['power']}

    while 1:
        # 退出检测
        if not gl.IS_SYS_QUIT:
            break
        try:
            sq = gl.MYQ.get(block=False)
            data = json.loads(sq)
            if data['op'] == 3:
                sqlite.add_imgdownload(
                    data['timestamp'], data['sqlstr'], data['path'])
            elif data['op'] == 7:
                cl.clean_ot_img()
        except Queue.Empty:
            time.sleep(1)
        except Exception, e:
            logger.error(e)
            time.sleep(1)

    del sqlite
    del cl


def loop_cleaner():
    """每隔30秒执行cleaner操作"""
    # 清理计数
    cl_count = 0
    while 1:
        # 退出检测
        if not gl.IS_SYS_QUIT:
            break
        else:
            try:
                if cl_count > 30:
                    cl_count = 0
                    sq = {}
                    sq['op'] = 7
                    gl.MYQ.put(json.dumps(sq))
            except Exception, e:
                logger.error(e)
        cl_count += 1
        time.sleep(1)


def version():
    """版本号"""
    return 'SX-UrlImgPackage V2.0.2;PORT:8017;'


def hello(environ, start_response):
    '''The WSGI_ application handler which returns an iterable
    over the "Hello World!" message.'''

    if (environ['REQUEST_METHOD'] == 'POST' and
            environ['PATH_INFO'] == '/urlimgpackage'):
        try:
            data = request_data(environ["wsgi.input"].read())
            status = '200 OK'
        except Exception as e:
            logger.error(e)
            data = ''
            status = '400 Error'
    else:
        data = json.dumps(
            {'package': None, 'msg': 'Request Error', 'code': 101})
        status = '400 Bad Request'

    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])


def server(description=None, **kwargs):
    '''

    Create the :class:`.WSGIServer` running :func:`hello`.

    '''

    description = description or 'Url Img Package Application'

    return wsgi.WSGIServer(hello, name='UrlImgPackageServer',
                           description=description, **kwargs)


def request_data(wsgi_input):
    data = urllib.unquote_plus(wsgi_input)
    post_data = urlparse.parse_qs(data, True)
    print post_data
    user_info = gl.KEYSDICT.get(post_data.get('key', [None])[0], None)

    if user_info is None:
        return json.dumps({'package': None, 'msg': 'Key Error', 'code': 105})

    _id = post_data.get('id', [None])[0]
    if _id is None:
        return json.dumps({'package': None, 'msg': 'No ID Parameter',
                          'code': 110})
    else:
        try:
            mysql = UMysql()
            res = mysql.get_urls_by_id(_id)
            url_list = json.loads(res['urls'])
        except Exception as e:
            logger.error(e)
            return json.dumps({'package': None, 'msg': 'SQL Error',
                              'code': 106})
        finally:
            del mysql

    gl.COUNT += 1
    imgd = Download()
    zipfile = imgd.main(url_list)
    del imgd

    return json.dumps({'package': zipfile, 'msg': 'Success', 'code': 100})


class PackageServer:

    def __init__(self):
        # 配置文件对象
        self.ini = ImgDownloadIni()
        self.sysini = self.ini.get_sys_conf()
        self.mysqlini = self.ini.ge_mysql_conf()
        # 基础路径 str
        gl.BASEPATH = self.sysini['path'].replace("/", "\\")
        # URL地址压缩队列 object
        gl.MYQ = Queue.Queue()

    def __del__(self):
        # 系统退出设为真
        gl.IS_SYS_QUIT = True
        
        del self.ini

    def create_mysql(self):
        """创建mysql线程池"""
        mysql_pool(self.mysqlini['host'], self.mysqlini[
                   'user'], self.mysqlini['passwd'], self.mysqlini['port'])

    def main(self):
        self.create_mysql()

        t1 = threading.Thread(target=sqlite_customer, args=())
        t2 = threading.Thread(target=loop_cleaner, args=())
        t1.start()
        t2.start()

        server().start()

if __name__ == '__main__':  # pragma nocover
    init_logging(r'log\imgdownload.log')
    logger = logging.getLogger('root')

    ps = PackageServer()
    ps.main()
    del ps
