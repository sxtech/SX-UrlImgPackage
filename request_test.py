# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

IP = '127.0.0.1'
PORT = 5000

def token_test():
    #auth = HTTPBasicAuth('admin','gdsx27677221')
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5000/token'
    data = {'username': 'test1', 'password': 'test12345'}
    r = requests.post(url, headers=headers, data=json.dumps(data))

    return r

def send_post(url, data, headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.post(url, data=data, headers=headers,
                      auth=HTTPBasicAuth('kakou', 'sx2767722'))

    return r

def package_post():
    url = 'http://{0}:{1}/package'.format(IP, PORT)
    headers = {'content-type': 'application/json'}
    data = {'urls': ['http://imgsrc.baidu.com/forum/w%3D580/sign=db88329813ce36d3a20483380af23a24/80f48d1001e93901a102437c7dec54e736d1961a.jpg']}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print r.status_code
    print r.text

if __name__ == '__main__':  # pragma nocover
    token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MjE3NDU1NCwiaWF0IjoxNDQyMTY3MzU0fQ.eyJzY29wZSI6WyJwYWNrYWdlX3Bvc3QiXSwidWlkIjoyM30.K63Ww6NF26XS6hHqDY5XceYYITkMpV6awLexEexSCbE'
    #r = token_test()
    package_post()


