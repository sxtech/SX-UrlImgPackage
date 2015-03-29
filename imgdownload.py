# -*- coding: cp936 -*-
import os
import sys
import time
import datetime
import logging
import threading
import zipfile
import Queue
import json

import gl
from helpfunc import HelpFunc

logger = logging.getLogger('root')

class Download:
    def __init__(self):
        self.hf = HelpFunc()  #辅助函数类
        
        self.basepath = gl.BASEPATH 
        self.timestamp = int(time.time())
        self.folder = str(self.timestamp)+'_'+str(gl.COUNT)
        self.path = os.path.join(self.basepath,self.folder)
        self.zipname = os.path.join(self.basepath,self.folder+'.zip')
        self.sqlstr = ''

        self.url_que = Queue.Queue()

        self.url_list = []
        #抓图线程数量
        self.thread_num = 4
        #抓图线程标记
        self.img_flag = False  
        
    def get_img_thread(self,m,i):
        for j in range(m,len(self.url_list),i):
            try:
                local = self.hf.get_img_by_url(self.url_list[j],self.path,'%s.jpg'%str(j))
                self.url_que.put(local)
            except Exception as e:
                logger.exception(e)
                print e

    def zip_thread(self):
        sq = {}
        sq['op'] = 3
        sq['timestamp'] = self.timestamp
        sq['sqlstr'] = ''
        sq['path'] = self.zipname
        gl.MYQ.put(json.dumps(sq))
        #创建文件夹
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        zipfp = zipfile.ZipFile(self.zipname, 'w')
        
        while 1:
            try:
                localpath = self.url_que.get(block=False)
                zipfp.write(localpath)
            except Queue.Empty:
                if self.img_flag:
                    break
                time.sleep(1)
            except Exception,e:
                logger.exception(e)
                time.sleep(1)
                
    def main(self,url_list):
        threads = []
        # 先创建线程对象
        self.url_list = url_list
        for i in range(self.thread_num):
            threads.append(threading.Thread(target=self.get_img_thread, args=(i,self.thread_num)))
        # 启动所有线程
        for t in threads:
            t.start()

        zip_t = threading.Thread(target=self.zip_thread, args=())
        zip_t.start()
        # 主线程中等待所有子线程退出
        for t in threads:
            t.join()
        self.img_flag = True

        zip_t.join()

        return self.folder+'.zip'

if __name__ == "__main__":    
    initLogging(r'log\imgdownload.log')
    logger = logging.getLogger('root')
    #fc = FtpCenter()
    #self.diskstate.checkDisk()
    #fc.getDisk()
    #print fc.activedisk
##    while True:
##        #print '123'
##        fc.checkDisk()
##        time.sleep(5)
    #fc.main()
