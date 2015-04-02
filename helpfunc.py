# -*- coding: cp936 -*-
import os
import urllib
import datetime

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UrlError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr('Url Error')
    
class HelpFunc:
    def getTime(self):
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    def ipToBigint(self,ipaddr):
        ipStrs = ipaddr.split(".")

        return str(int(ipStrs[3]) + int(ipStrs[2])*256 + int(ipStrs[1])*256*256 + int(ipStrs[0])*256*256*256) 

    def bigintToIp(self,intStr):
        bigint = int(intStr)

        first = bigint/(256*256*256)
        rest = bigint - (first*256*256*256)
        
        second = rest/(256*256)
        rest -= second*256*256
        
        third = rest/256    
        fourth = rest - third * 256
        
        return "%d.%d.%d.%d"%(first,second,third,fourth)

    #根据URL地址获取图片到本地
    def get_img_by_url(self,url,path,filename):
        try:
            local = os.path.join(path,filename)
            filename,headers = urllib.urlretrieve(url.replace('\\','/').encode('utf8'),local)

            if headers.getheader('Content-Type') != 'image/jpeg':
                raise UrlError(url)
            return filename
        except Exception as e:
            raise UrlError(url)
        
if __name__ == '__main__':
    hf = HelpFunc()
    print hf.getTime()
