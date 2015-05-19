# -*- coding: utf-8 -*-
import time

from peewee import *

import gl

gl.DB = SqliteDatabase('package.db', journal_mode='WAL')


class BaseModel(Model):
    class Meta:
        database = gl.DB

    @classmethod
    def get_one(cls, *query, **kwargs):
    #为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        try:
            return cls.get(*query,**kwargs)
        except DoesNotExist:
            return None


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    banned = BooleanField(default=False)


class Package(BaseModel):
    timeflag = IntegerField(default=int(time.time()))
    ip = TextField()
    path = TextField()
    banned = BooleanField(default=False)

    class Meta:
        indexes = (
            # create a non-unique on banned/timeflag
            (('banned','timeflag'), False),
        )

