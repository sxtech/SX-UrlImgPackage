# -*- coding: utf-8 -*-
import os
import zipfile
import random

from gevent import monkey
import gevent

from img_package import app, logger
import helper


"""

使用gevent爬图并压缩

"""


class Downloader(object):

    def __init__(self):
        # 基础路径 str
        self.basepath = app.config['BASEPATH']
        # 文件夹名,随机产生32位16进制数字 str
        self.folder = "%032x" % random.getrandbits(128)
        # 文件路径 str
        self.path = os.path.join(self.basepath, self.folder)
        # zip压缩文件名 str
        self.zipname = os.path.join(self.basepath, self.folder + '.zip')

        # 创建文件夹
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def fetch_imgs(self, url_list):
        """gevent抓取图像"""
        join_list = []
        count = 1
        for url in url_list:
            join_list.append(gevent.spawn(
                helper.get_url_img, url,
                os.path.join(self.path,'%s.jpg' % count)))
            count += 1
        gevent.joinall(join_list)

    def create_zip(self):
        """创建ZIP压缩"""
        # 创建压缩文件对象
        zipfp = zipfile.ZipFile(self.zipname, 'w')
        # 从文件夹中获取图片文件并压缩
        for d in os.listdir(self.path):
            zipfp.write(os.path.join(self.path, d))

    def main(self, url_list):
        """主函数"""
        self.fetch_imgs(url_list)
        self.create_zip()

        return {'zipname': self.zipname, 'name': self.folder + '.zip'}


##if __name__ == "__main__":
    
