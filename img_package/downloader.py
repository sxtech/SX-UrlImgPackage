# -*- coding: utf-8 -*-
import os
import uuid
import zipfile
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
        self.basepath = basepath
        # 文件夹名, uuid1 str
        self.folder = uuid.uuid1().hex
        # 文件路径 str
        self.path = os.path.join(self.basepath, self.folder)
        # zip压缩文件名 str
        self.zipname = os.path.join(self.basepath, self.folder + '.zip')
        # multiprocessing child管道
	self.conn = conn
	# url地址列表 list
	self.url_list = url_list

        # 创建文件夹
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def fetch_imgs(self, url_list):
        """requests长连接抓取图像"""
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

    
