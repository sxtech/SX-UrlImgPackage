# -*- coding: utf-8 -*-
import json
import unittest

import arrow

from img_package import db
from img_package.models import Users, Scope, Package


class TestModelPackage(unittest.TestCase):

    def test_get(self):
        p = Package.query.filter(Package.id==2).first()
        self.assertEqual(p.ip, '127.0.0.1')
        self.assertEqual(p.path[-4:], '.zip')

    def test_set(self):
        db.session.query(Package).filter(Package.id==2).update({'banned': 2})
        db.session.commit()

    def test_add(self):
        p = Package(ip='127.0.0.1', path='c:\\test\\test.zip',
                    date_created=arrow.now().datetime,
                    expired=arrow.now().timestamp+600, banned=0)
        db.session.add(p)
        db.session.commit()
        self.assertTrue(isinstance(p.id, int))

if __name__ == "__main__":
    #hbcall_test()
    #vehicle_test()
    #join_test(u'LC6879', '02')
    #test_package_add()
    #test_package_get()
    #test_package_set()
    unittest.main()
                            
