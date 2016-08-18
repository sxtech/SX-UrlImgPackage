# -*- coding: utf-8 -*-
import os
import shutil
import threading
import logging

import arrow

from models import Package
from img_package import app, db, logger


class CleanWorker:

    def __init__(self):
        logger.info('CleanWorker start')

    def __del__(self):
        logger.info('CleanWorker quit')

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
        t = arrow.now().timestamp

        packages = Package.query.filter(
            Package.expired < t, Package.banned==0).all()
        for i in packages:
            if i.path is not None and i.path != '':
                self.clean_file(i.path)
                logger.warning('%s has been removed!' % i.path)
            db.session.query(Package).filter(Package.id==i.id).update({'banned' : 1})
            db.session.commit()

    def loop_clean(self):
        """sqlite数据库操作执行线程"""
        # 清理计数
        count = 0
        while 1:
            # 退出检测
            if app.config['IS_QUIT']:
                break
            try:
                # 每30秒清除超时图片文件
                if count > 30:
                    self.clean_ot_img()
                    count = 0
            except Exception as e:
                logger.error(e)
                time.sleep(1)
            finally:
                count += 1

    def main(self):
        t = threading.Thread(target=self.loop_clean, args=())
        t.start()
