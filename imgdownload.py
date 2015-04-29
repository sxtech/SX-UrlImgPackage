# -*- coding: utf-8 -*-
import os
import time
import logging
import threading
import zipfile
import Queue
import json

import gl
from logbook import Logger
from requests_func import RequestsFunc

log = Logger('Package')

"""

多线程抓图并压缩

"""


class Download:

    def __init__(self, ip='127.0.0.1'):
        # 请求IP
        self.ip = ip
        # HTTP函数类
        self.rf = RequestsFunc()
        # 基础路径 str
        self.basepath = gl.BASEPATH
        # 时间戳 int
        self.timestamp = int(time.time())
        # 文件夹名 str
        self.folder = str(self.timestamp) + '_' + str(gl.COUNT)
        # 文件路径 str
        self.path = os.path.join(self.basepath, self.folder)
        # zip压缩文件名 str
        self.zipname = os.path.join(self.basepath, self.folder + '.zip')
        # URL地址压缩队列 object
        self.url_que = Queue.Queue()
        # URL地址 list
        self.url_list = []
        # 抓图线程数量 int
        self.threads_int = 8
        # 抓图线程退出标记 bool
        self.is_quit = False

    def get_img_thread(self, m, i):
        """抓图线程"""
        for j in range(m, len(self.url_list), i):
            try:
                filename = os.path.join(self.path, '%s.jpg' % str(j))
                self.rf.get_url_img(self.url_list[j], filename)
                self.url_que.put(filename)
            except Exception as e:
                log.error('%s: %s' % (e, self.url_list[j]))

    def zip_thread(self):
        """ZIP压缩线程"""
        sq = {}
        sq['timestamp'] = self.timestamp
        sq['ip'] = self.ip
        sq['path'] = self.zipname
        gl.MYQ.put(json.dumps(sq))
        # 创建文件夹
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # 创建压缩文件对象
        zipfp = zipfile.ZipFile(self.zipname, 'w')
        # 从url队列中获取图片文件并压缩
        while 1:
            try:
                img_file = self.url_que.get(timeout=1)
                zipfp.write(img_file)
            except Queue.Empty:
                if self.is_quit:
                    break
            except Exception, e:
                log.error(e)
                time.sleep(1)

    def main(self, url_list):
        """主函数"""
        # 存放线程对象list
        threads = []
        # 先创建线程对象
        self.url_list = url_list
        for i in range(self.threads_int):
            threads.append(
                threading.Thread(target=self.get_img_thread,
                                 args=(i, self.threads_int)))
        # 启动抓图线程
        for t in threads:
            t.start()
        # 压缩文件线程
        zip_t = threading.Thread(target=self.zip_thread, args=())
        zip_t.start()
        # 主线程中等待所有子线程退出
        for t in threads:
            t.join()
        # 退出标记设为真
        self.is_quit = True

        zip_t.join()

        return self.folder + '.zip'

if __name__ == "__main__":
    print '123'
