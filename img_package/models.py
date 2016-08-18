# -*- coding: utf-8 -*-
import arrow

from . import db


class Users(db.Model):
    """用户管理"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(128))
    scope = db.Column(db.String(128), default='')
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    date_modified = db.Column(db.DateTime, default=arrow.now().datetime)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, scope='', banned=0,
                 date_created=None, date_modified=None):
        self.username = username
        self.password = password
        self.scope = scope
        now = arrow.now().datetime
        if not date_created:
            self.date_created = now
        if not date_modified:
            self.date_modified = now
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id


class Scope(db.Model):
    """权限范围"""
    __tablename__ = 'scope'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Scope %r>' % self.id


class Package(db.Model):
    """图片打包"""
    __tablename__ = 'package'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(16))
    path = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    expired = db.Column(db.Integer, default=arrow.now().timestamp+1800)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, ip, path, date_created=None, expired=None, banned=0):
        self.ip = ip
        self.path = path
        if date_created is None:
            self.date_created = arrow.now().datetime
        else:
            self.date_created = date_created
        if not expired:
            self.expired = arrow.now().timestamp + 1800
        else:
            self.expired = expired
        self.banned = banned

    def __repr__(self):
        return '<Package %r>' % self.id

