# -*- coding: utf-8 -*-
import os
import json
import time
import datetime
import shutil
import threading
import Queue
import logging

import gl
from models import Package


logger = logging.getLogger('root')


class PackageWorker:

    def __init__(self):
        # URL地址压缩队列 object
        gl.MYQ = Queue.Queue()
        # 数据库对象
        self.db = gl.DB
        # 15分钟间隔
        self.delta = 15

    def __del__(self):
        # 系统退出设为真
        gl.IS_SYS_QUIT = True

        del self.ini

    def clean_file(self, filename):
        """删除文件"""
        try:
            os.remove(filename)
        except Exception, e:
            logger.error(e)
        try:
            shutil.rmtree(filename[:-4])
        except Exception, e:
            logger.error(e)

    def clean_ot_img(self):
        """删除超时图片文件"""
        _time = time.time() - \
            datetime.timedelta(minutes=self.delta).total_seconds()
        
        self.db.connect()

        packages = (Package
                    .select()
                    .where((Package.banned == 0) & (Package.timeflag < int(_time))))

        for i in packages:
            if i.path is not None and i.path != '':
                self.clean_file(i.path)
                logger.warning('Cleaned %s' % i.path)
            q = Package.update(banned=True).where(Package.id == i.id)
            q.execute()  # Execute the query, updating the database.

        self.db.close()

    def clean_work(self):
        """sqlite数据库操作执行线程"""
        # 清除文件类对象

        # 清理计数
        count = 0
        while 1:
            # 退出检测
            if gl.IS_SYS_QUIT:
                break
            try:
                if count > 30:
                    self.clean_ot_img()
                    count = 0
            except Exception as e:
                logger.error(e)
                time.sleep(1)
            finally:
                count += 1

    def main(self):
        t = threading.Thread(target=self.clean_work, args=())
        t.start()



