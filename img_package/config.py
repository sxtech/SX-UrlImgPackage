# -*- coding: utf-8 -*-
import os


class Config(object):
    # 密码 string
    SECRET_KEY = 'hellokitty'
    # 服务器名称
    HEADER_SERVER = 'SX-UrlImgPackage'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认1小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../package.db'
    # 数据库连接 dict
    # SQLALCHEMY_BINDS = {}
    # 用户权限范围 dict
    SCOPE_USER = {}
    # 白名单启用 bool
    WHITE_LIST_OPEN = True
    # 白名单列表 set
    WHITE_LIST = set(['127.0.0.1'])
    # 文件路径
    BASEPATH = '/home/imgpackage'
    # nginx静态文件服务IP
    SERVER_ADDR = '10.47.223.147:8098'
    # 退出标记
    IS_QUIT = False


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
