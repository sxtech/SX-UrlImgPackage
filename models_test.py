# -*- coding: utf-8 -*-
import json

import arrow

from img_package import db
from img_package.models import Users, Scope, Package


def test_package_add():
    info = {
        'ip': '127.0.0.1',
        'date_created': str(arrow.now().format('YYYY-MM-DD HH:mm:ss')),
        'path': 'c:\\test\\test.zip'
    }
    p = Package(ip='127.0.0.1',path='c:\\test\\test.zip',
                date_created = arrow.now().datetime,
                expired=arrow.now().timestamp+600, banned=0)
    db.session.add(p)
    db.session.commit()
    print p.id

def test_package_get():
    p = Package.query.filter(
        Package.expired > 1458214367, Package.banned == 0).all()
    for i in p:
        print i.ip
        print i.path
        print i.date_created
        print i.expired
        print i.banned

def test_package_set():
    db.session.query(Package).filter(Package.id == 1).update({'banned' : 2})
    db.session.commit()
    
if __name__ == "__main__":
    #hbcall_test()
    #vehicle_test()
    #join_test(u'LC6879', '02')
    #test_package_add()
    #test_package_get()
    test_package_set()
                            
