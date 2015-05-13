# -*- coding: utf-8 -*-
import os
import json
import time
import threading
import Queue
import logging

import gl
from iniconf import MyIni
from sqlitedb import USqlite
from cleaner import Cleaner


logger = logging.getLogger('root')


class PackageWorker:

    def __init__(self):
        # 配置文件对象
        self.ini = MyIni()
        self.sysini = self.ini.get_sys_conf()
        # 基础路径 str
        gl.BASEPATH = self.sysini['path'].replace("/", "\\")
        # URL地址压缩队列 object
        gl.MYQ = Queue.Queue()

        logger.warning('Sys Start')

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



