# -*- coding: utf-8 -*-
import os
import time
import datetime
import shutil

from logbook import Logger

log = Logger('Package')


class Cleaner:

    def __init__(self, sqliteobj):
        self.sqlite = sqliteobj
        self.delta = 0.5

    def clean_file(self, filename):
        """删除文件"""
        try:
            os.remove(filename)
        except Exception, e:
            log.error('file: %s; error: %s'%(filename,e))
        try:
            shutil.rmtree(filename[:-4])
        except Exception, e:
            log.error('file: %s; error: %s'%(filename,e))

    def clean_ot_img(self):
        """删除超时图片文件"""
        _time = time.time() - \
            datetime.timedelta(hours=self.delta).total_seconds()
        s = self.sqlite.get_imgdownload(int(_time), 0)

        if s != []:
            for i in s:
                if i['path'] is not None and i['path'] != '':
                    logger.info('Cleaned %s' % i['path'])
                    self.clean_file(i['path'])
                self.sqlite.update_imgdownload_by_id(i['id'])

    def main(self):
        while True:
            try:
                self.clean_ot_img()
            except Exception, e:
                log.error(e)
            time.sleep(60)

if __name__ == "__main__":
    from sqlitedb import USqlite
    s = USqlite()
    cl = Cleaner(s)
    cl.main()
    cl.clean_ot_img()

    del cl
