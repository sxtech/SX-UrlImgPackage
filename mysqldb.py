# -*- coding: cp936 -*-
import MySQLdb
import gl

class UMysql:
    def __init__(self):
        self.conn = gl.MYSQLPOOL.connection()
        self.cur  = self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        
    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception,e:
            pass

    def add_urls(self,values):
        try:
            self.cur.executemany("INSERT INTO url_json (time,urls) VALUES(%s,%s)",values)
        except MySQLdb.Error,e:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()

    def get_urls_by_id(self,_id):
        try:
            self.cur.execute("SELECT * FROM url_json WHERE id=%s"%_id)
            s = self.cur.fetchone()
            self.conn.commit()
        except MySQLdb.Error,e:
            self.conn.rollback()
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
    from DBUtils.PooledDB import PooledDB
    import datetime
    import threading
    
    def mysqlPool(h,u,ps,pt,minc=5,maxc=20,maxs=10,maxcon=100,maxu=1000):
        gl.MYSQLPOOL = PooledDB(
            MySQLdb,
            host = h,
            user = u,
            passwd = ps,
            db = "img_url",
            charset = "utf8",
            mincached = minc,        #启动时开启的空连接数量
            maxcached = maxc,        #连接池最大可用连接数量
            maxshared = maxs,        #连接池最大可共享连接数量
            maxconnections = maxcon, #最大允许连接数量
            maxusage = maxu)

    mysqlPool('localhost','root','',3306)
    
    mysql = UMysql()
    values=[(datetime.datetime.now(),'["123","456"]')]
    s = mysql.get_urls_by_id(1)
    print s
    del mysql
    

    

