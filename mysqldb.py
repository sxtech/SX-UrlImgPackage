# -*- coding: utf-8 -*-
import MySQLdb

import gl

"""

mysql类

"""


class UMysql:

    def __init__(self):
        self.conn = gl.MYSQLPOOL.connection()
        self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception:
            pass

    def add_urls(self, values):
        """Add json format url like '["http://..","h.."]' and return None."""
        try:
            self.cur.executemany(
                "INSERT INTO url_json (time,urls) VALUES(%s,%s)", values)
        except MySQLdb.Error:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def get_urls_by_id(self, _id):
        """Get json format url by id and return tuple."""
        try:
            self.cur.execute("SELECT * FROM url_json WHERE id=%s" % _id)
            s = self.cur.fetchone()
            self.conn.commit()
        except MySQLdb.Error:
            self.conn.rollback()
            raise
        else:
            return s

    def end_of_cur(self):
        self.conn.commit()

    def sql_commit(self):
        self.conn.commit()

    def sql_rollback(self):
        self.conn.rollback()

if __name__ == "__main__":
    from DBUtils.PooledDB import PooledDB
    import datetime

    def mysql_pool(h, u, ps, pt,
                   minc=5, maxc=20, maxs=10, maxcon=100, maxu=1000):
        gl.MYSQLPOOL = PooledDB(
            MySQLdb,
            host=h,
            user=u,
            passwd=ps,
            db="img_url",
            charset="utf8",
            mincached=minc,
            maxcached=maxc,
            maxshared=maxs,
            maxconnections=maxcon,
            maxusage=maxu
        )

    mysql_pool('localhost', 'root', '', 3306)

    mysql = UMysql()
    values = [(datetime.datetime.now(), '["123","456"]')]
    s = mysql.get_urls_by_id(1)
    print s
    del mysql
