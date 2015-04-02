#-*- encoding: gb2312 -*-
import ConfigParser
import string, os, sys

class ImgDownloadIni:
    def __init__(self,confpath = 'imgdownload.conf'):
        self.path = ''
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def get_sys_conf(self):
        sysconf = {}
        sysconf['path'] = self.cf.get('SYSSET','path')
        sysconf['port'] = self.cf.getint('SYSSET','port')
        return sysconf

    def ge_mysql_conf(self):
        mysqlconf = {}
        mysqlconf['host']    = self.cf.get('MYSQLSET','host')
        mysqlconf['user']    = self.cf.get('MYSQLSET','user')
        mysqlconf['passwd']  = self.cf.get('MYSQLSET','passwd')
        mysqlconf['port']    = self.cf.getint('MYSQLSET','port')
        mysqlconf['mincached']      = self.cf.getint('MYSQLSET','mincached')
        mysqlconf['maxcached']      = self.cf.getint('MYSQLSET','maxcached')
        mysqlconf['maxshared']      = self.cf.getint('MYSQLSET','maxshared')
        mysqlconf['maxconnections'] = self.cf.getint('MYSQLSET','maxconnections')
        mysqlconf['maxusage']       = self.cf.getint('MYSQLSET','maxusage')
        
        return mysqlconf

     
if __name__ == "__main__":

    try:
        img = ImgDownloadIni()
        s= img.ge_mysql_conf()
        print s
        #print (s['path'].replace("/","\\"),1)
        #s = imgIni.getPlateInfo(PATH2)
        #i = s['host'].split(',')
        #print s
        #disk = s['disk'].split(',')
        #print disk
        #del i
    except ConfigParser.NoOptionError,e:
        print e
        time.sleep(10)
