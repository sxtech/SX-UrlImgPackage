# -*- coding: utf-8 -*-

from httplib2 import Http  
from urllib import urlencode
import httplib2
import json
import requests
from requests.auth import HTTPDigestAuth


def TestHttpPost():
  word=u'美国'.encode('utf8')
  urlstr = 'http://127.0.0.1:8017/package'
  
  json_data = json.dumps(['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg'])
  #print json_data
  data={'key':'sx2767722','urls': json_data} 
  
  h = httplib2.Http('.cache')
  response,content = h.request(urlstr, 'POST', urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})  

  print(response,content)

def send_post(url, send_data, headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.post(url, data=send_data, headers=headers)

    return r
  
if __name__ == '__main__':  # pragma nocover
  #TestHttpPost()
  urlstr = 'http://127.0.0.1:8017/package'
  json_data = json.dumps(['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg'])
  data={'key':'sx2767722!','urls': ['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg']}
  
  r = send_post(urlstr, json.dumps(data))
  print r.status_code
  print r.text
