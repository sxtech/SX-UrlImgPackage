﻿# -*- coding: utf-8 -*-
import os
import zipfile
import random
import multiprocessing

import requests

import helper


"""

使用requests爬图并压缩

"""


class Downloader(multiprocessing.Process):

    def __init__(self, conn, basepath, url_list):
	multiprocessing.Process.__init__(self)
        # 基础路径 str
        self.basepath = basepath #app.config['BASEPATH']
        # 文件夹名,随机产生32位16进制数字 str
        self.folder = "%032x" % random.getrandbits(128)
        # 文件路径 str
        self.path = os.path.join(self.basepath, self.folder)
        # zip压缩文件名 str
        self.zipname = os.path.join(self.basepath, self.folder + '.zip')
	self.conn = conn
	# url地址列表
	self.url_list = url_list

        # 创建文件夹
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def fetch_imgs(self, url_list):
        """gevent抓取图像"""
	s = requests.Session()
	count = 1
	for url in url_list:
	    helper.get_url_img(url, os.path.join(self.path,'%s.jpg' % count), s)
	    count += 1

    def create_zip(self):
        """创建ZIP压缩"""
        # 创建压缩文件对象
        zipfp = zipfile.ZipFile(self.zipname, 'w', zipfile.ZIP_STORED)
        # 从文件夹中获取图片文件并压缩
        for d in os.listdir(self.path):
            zipfp.write(os.path.join(self.path, d))

    def run(self):
        """主函数"""
        self.fetch_imgs(self.url_list)
        self.create_zip()
	self.conn.send({'zipname': self.zipname, 'name': self.folder + '.zip'})
	self.conn.close()

    
