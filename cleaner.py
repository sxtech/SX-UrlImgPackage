import os
import time
import datetime
import logging
import sqlite3

import gl

logger = logging.getLogger('root')
    
class Cleaner:
    def __init__(self,sqliteobj):
        self.sqlite = sqliteobj
        self.delta = 0.5

    def clean_file(self,filename):
        try:
            os.remove(filename)
        except Exception,e:
            logger.error(e)
        try:
            os.rmdir(filename[:-4])
        except Exception,e:
            logger.error(e)
    
    def clean_ot_img(self):
        _time = time.time()-datetime.timedelta(hours=self.delta).total_seconds()
        s = self.sqlite.get_imgdownload(int(_time),0)
        
        if s != []:
            for i in s:
                if i['path'] != None and i['path'] != '':
                    print 'clean %s'%i['path']
                    self.clean_file(i['path'])
                self.sqlite.update_imgdownload_by_id(i['id'])

    def main(self):
        while True:
            try:
                self.clean_ot_img()
            except Exception,e:
                logger.error(e)
            time.sleep(60)

if __name__ == "__main__":
    from sqlitedb import USqlite
    s = USqlite()
    cl = Cleaner(s)
    cl.main()
    cl.clean_ot_img()

    del cl
