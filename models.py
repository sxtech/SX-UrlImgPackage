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
            (('banned','timeflag'),True),
        )

if __name__ == '__main__':
    #db = SqliteDatabase('package.db', journal_mode='WAL')
    #db.connect()
    #u = User.select().where(User.username == 'fire')
    #db = SqliteDatabase('package.db', journal_mode='WAL')
    db = gl.DB
    db.connect()
    #db.create_tables([User,Package])
##    package = (Package
##             .select()
##             .where(Package.timeflag < 12))
##    package = (Package
##               .select()
##               .where((Package.banned == 0) & (Package.timeflag < 12345)))
##    #print type(query)
##    for i in package:
##        print i.id
    q = Package.update(banned=True).where(Package.id == 1)
    q.execute()
    db.close()
    #grandma = User.get_one(User.username == '23')
    #print grandma.id
##    #print u
##    for i in u:
##        print i.id
##    try:
##        db.create_tables([User,Package])
##    except OperationalError as e:
##        print e
##
##res = User.get_user_list()
##print res
