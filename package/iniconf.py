# -*- coding: utf-8 -*-
import ConfigParser

"""

配置文件类

"""


class MyIni:

    def __init__(self, confpath='package.conf'):
        self.path = ''
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def get_sys_conf(self):
        """系统参数"""
        conf = {}
        conf['path'] = self.cf.get('SYSSET', 'path')
        conf['port'] = self.cf.getint('SYSSET', 'port')
        
        return conf
