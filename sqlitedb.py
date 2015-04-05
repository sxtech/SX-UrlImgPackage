# -*- coding: utf-8 -*-
import sqlite3

"""

sqlite3类

"""


def dict_factory(cursor, row):
    """sqlite返回字典类型"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class USqlite:

    def __init__(self):
        self.conn = sqlite3.connect("imgdownload.db", check_same_thread=False)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()

    def __del__(self):
        try:
            self.conn.close()
            self.cur.close()
        except:
            pass

    def create_table(self):
        """"Initialize table if not exists."""
        sql = '''CREATE TABLE IF NOT EXISTS "user" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "key"  TEXT,
                "priority"  INTEGER NOT NULL DEFAULT 10,
                "power"  INTEGER NOT NULL DEFAULT 4,
                "mark"  TEXT
                );

                CREATE UNIQUE INDEX IF NOT EXISTS "idx_key"
                ON "user" ("key" ASC);

                CREATE TABLE IF NOT EXISTS "imgdownload" (
                "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "timeflag"  INTEGER,
                "ip"  TEXT,
                "path"  TEXT,
                "banned"  INTEGER NOT NULL DEFAULT 0
                );

                CREATE INDEX IF NOT EXISTS "index_banned"
                ON "imgdownload" ("banned" ASC, "timeflag" DESC);
                '''
        self.cur.executescript(sql)
        self.conn.commit()

    def get_users(self):
        """Get users from table 'user' and return list"""
        try:
            self.cur.execute("select * from user")
            s = self.cur.fetchall()
            self.conn.commit()
            return s
        except sqlite3.Error:
            raise

    def get_user_by_key(self, key):
        """Get user by key and return tuple"""
        try:
            self.cur.execute("select * from user where key='%s'" % key)
            s = self.cur.fetchone()
            self.conn.commit()
            return s
        except sqlite3.Error:
            raise

    def get_imgdownload(self, _time, banned=0):
        """Get imgdownload by time and return list"""
        try:
            self.cur.execute("select * from imgdownload where banned=%s and \
                              timeflag<=%s" % (banned, _time))
            s = self.cur.fetchall()
        except sqlite3.Error:
            raise
        else:
            self.conn.commit()
            return s

    def update_imgdownload_by_id(self, id, banned=1):
        """Edit table 'imgdownload' by id and return None"""
        try:
            self.cur.execute("update imgdownload set banned=%s \
                              where id=%s" % (banned, id))
            self.conn.commit()
        except sqlite3.Error:
            raise

    def add_imgdownload(self, _time, ip, path=''):
        """Add a imgdownload info and return insert id as tuple"""
        try:
            self.cur.execute("INSERT INTO imgdownload(timeflag,ip,path) \
                              VALUES(%s,'%s','%s')" % (_time, ip, path))
            self.cur.execute("SELECT last_insert_rowid()")
            self.conn.commit()
            s = self.cur.fetchone()
        except sqlite3.Error:
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
    sl = USqlite()
    sl.create_table()
    print sl.get_users()

    del sl
