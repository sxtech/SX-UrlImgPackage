# -*- coding: utf-8 -*-
import ConfigParser

"""

配置文件类

"""


class ImgDownloadIni:

    def __init__(self, confpath='imgdownload.conf'):
        self.path = ''
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def get_sys_conf(self):
        """系统参数"""
        sysconf = {}
        sysconf['path'] = self.cf.get('SYSSET', 'path')
        sysconf['port'] = self.cf.getint('SYSSET', 'port')
        return sysconf

    def test(self):
        #return self.cf.has_option('SYSSET', 'port')
        #return self.cf.items('SYSSET')
        try:
            path = self.cf.get('SYSSET', 'path2')
        except ConfigParser.Error as e:
            print '123e'
            print e


if __name__ == "__main__":

    try:
        img = ImgDownloadIni()
        s = img.test()
        print s
    except ConfigParser.NoOptionError, e:
        print e
