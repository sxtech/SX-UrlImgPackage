# -*- coding: utf-8 -*-

import os
import json
import time
import threading
import Queue
import logging
import logging.handlers

from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Api
from flask_restful import Resource

import gl
from imgdownload import Download
from iniconf import ImgDownloadIni
from sqlitedb import USqlite
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


def version():
    """版本号"""
    return 'SX-UrlImgPackage V3.2.0'


app = Flask(__name__)
api = Api(app)


class Hello(Resource):

    def get(self):
        return {'message': "Welcome to use %s" % version()}


class TodoList(Resource):

    def post(self):
        if not request.json:
            return {'package': None, 'msg': 'Bad Request', 'code': 400}, 400
        if request.json.get('key', None) not in gl.KEYSDICT:
            return {'package': None, 'msg': 'Key Error', 'code': 105}, 400
        if 'urls' not in request.json:
            return {'package': None, 'msg': 'No "urls" key', 'code': 106}, 400

        gl.COUNT += 1
        imgd = Download(request.remote_addr)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'package': zipfile, 'msg': 'Success', 'code': 100}, 201


api.add_resource(Hello, '/')
api.add_resource(TodoList, '/package')


class PackageServer:

    def __init__(self):
        # 配置文件对象
        self.ini = ImgDownloadIni()
        self.sysini = self.ini.get_sys_conf()
        # 基础路径 str
        gl.BASEPATH = self.sysini['path'].replace("/", "\\")
        # URL地址压缩队列 object
        gl.MYQ = Queue.Queue()

    def __del__(self):
        # 系统退出设为真
        gl.IS_SYS_QUIT = True
        logger.warning('Sys Quit')
        del self.ini

    def sqlite_customer(self):
        """sqlite数据库操作执行线程"""
        # 创建sqlite对象
        sqlite = USqlite()
        # 创建数据库表
        sqlite.create_table()
        # 清除文件类对象
        cl = Cleaner(sqlite)
        for i in sqlite.get_users():
            gl.KEYSDICT[i['key']] = {'priority': i['priority'],
                                     'power': i['power']}

        # 清理计数
        cl_count = 0
        while 1:
            # 退出检测
            if gl.IS_SYS_QUIT:
                break
            try:
                sq = gl.MYQ.get(timeout=1)
                data = json.loads(sq)
                sqlite.add_imgdownload(
                    data['timestamp'], data['ip'], data['path'])

                if cl_count > 30:
                    cl.clean_ot_img()
                    cl_count = 0
            except Queue.Empty:
                pass
            except Exception, e:
                logger.error(e)
                time.sleep(1)
            finally:
                cl_count += 1

        del sqlite
        del cl

    def main(self):
        t = threading.Thread(target=self.sqlite_customer, args=())
        t.start()

        app.run(host="0.0.0.0", port=self.sysini.get('port', 8017))

if __name__ == '__main__':  # pragma nocover
    init_logging(r'log\imgdownload.log')
    logger = logging.getLogger('root')

    ps = PackageServer()
    ps.main()
    del ps
