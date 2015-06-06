# -*- coding: utf-8 -*-
import os


class Config(object):
    DEBUG = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    # 主机IP
    HOST = '0.0.0.0'
    # 端口
    PORT = '8017'
    # 数据库名称
    DATABASE = 'package.db'
    # 文件路径
    BASEPATH = 'imgpackage'

class Develop(Config):
    pass

class Production(Config):
    DEBUG = False
