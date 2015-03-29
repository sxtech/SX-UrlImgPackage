# -*- coding: cp936 -*-
import sqlite3
import datetime
import gl

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class USqlite:
    def __init__(self):
        self.conn = sqlite3.connect("imgdownload.db",check_same_thread = False)
        self.conn.row_factory = dict_factory
        self.cur  = self.conn.cursor()
            
    def __del__(self):
        try:
            self.conn.close()
            self.cur.close()
        except Exception,e:
            pass

    def create_table(self):
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

    #获取用户信息
    def get_users(self):
        try:
            self.cur.execute("select * from user")
            s = self.cur.fetchall()
            self.conn.commit()
            return s
        except sqlite3.Error as e:
            raise

    #根据key查询用户信息
    def get_user_by_key(self,key):
        try:
            self.cur.execute("select * from user where key='%s'"%key)
            s = self.cur.fetchone()
            self.conn.commit()
            return s
        except sqlite3.Error as e:
            raise

    #1
    #根据条件获取图片下载记录
    def get_imgdownload(self,_time,banned=0):
        try:
            self.cur.execute("select * from imgdownload where banned=%s and timeflag<=%s"%(banned,_time))
            s = self.cur.fetchall()
        except sqlite3.Error as e:
            raise
        else:
            self.conn.commit()
            return s

    #2
    #根据ID更新图片下载记录
    def update_imgdownload_by_id(self,id,banned=1):
        try:
            self.cur.execute("update imgdownload set banned=%s where id=%s"%(banned,id))
            self.conn.commit()
        except sqlite3.Error as e:
            raise

    #3
    #添加一条图片下载记录并返回ID
    def add_imgdownload(self,_time,ip,path=''):
        try:
            self.cur.execute("INSERT INTO imgdownload(timeflag,ip,path) VALUES(%s,'%s','%s')"%(_time,ip,path))
            self.cur.execute("SELECT last_insert_rowid()")
            self.conn.commit()
            s = self.cur.fetchone()
        except sqlite3.Error as e:
            raise
        else:
            return s
        
    def endOfCur(self):
        self.conn.commit()
        
    def sqlCommit(self):
        self.conn.commit()
        
    def sqlRollback(self):
        self.conn.rollback()
            
if __name__ == "__main__":
    sl = USqlite()
    sl.create_table()
    print sl.get_imgdownload(123)

    del sl


