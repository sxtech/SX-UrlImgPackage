# -*- coding: utf-8 -*-

from httplib2 import Http  
from urllib import urlencode
import httplib2
import json


def TestHttpPost():
  word=u'美国'.encode('utf8')
  urlstr = 'http://127.0.0.1:8017/urlimgpackage'
  
  json_data = json.dumps(['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg'])
  #print json_data
  data={'key':'sx2767722','id': 1} 
  
  h = httplib2.Http('.cache')
  response,content = h.request(urlstr, 'POST', urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})  

  print(response,content)
  
if __name__ == '__main__':  # pragma nocover
  TestHttpPost()
