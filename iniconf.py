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

    def ge_mysql_conf(self):
        """mysql参数"""
        mysqlconf = {}
        mysqlconf['host'] = self.cf.get('MYSQLSET', 'host')
        mysqlconf['user'] = self.cf.get('MYSQLSET', 'user')
        mysqlconf['passwd'] = self.cf.get('MYSQLSET', 'passwd')
        mysqlconf['port'] = self.cf.getint('MYSQLSET', 'port')
        mysqlconf['mincached'] = self.cf.getint('MYSQLSET', 'mincached')
        mysqlconf['maxcached'] = self.cf.getint('MYSQLSET', 'maxcached')
        mysqlconf['maxshared'] = self.cf.getint('MYSQLSET', 'maxshared')
        mysqlconf['maxconnections'] = self.cf.getint(
            'MYSQLSET', 'maxconnections')
        mysqlconf['maxusage'] = self.cf.getint('MYSQLSET', 'maxusage')

        return mysqlconf


if __name__ == "__main__":

    try:
        img = ImgDownloadIni()
        s = img.ge_mysql_conf()
        print s
    except ConfigParser.NoOptionError, e:
        print e
