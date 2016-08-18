# -*- coding: utf-8 -*-
import gevent
from gevent.event import AsyncResult

a = AsyncResult()

def xiaodi():
    """
    一会堵上10秒 ！
    """
    print "xiaodi 开始"
    gevent.sleep(10)
    a.set('hello world')
    print "xiaodi 结束"

def dage():
    """
    需要等待xiaodi完事了后，他才能i live
    """
    print 'dage 这里是先开始的...'
    print a.get() # blocking
    print 'I live!'

gevent.joinall([
    gevent.spawn(xiaodi),
    gevent.spawn(dage)
])
