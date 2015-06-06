# -*- coding: utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth

def send_post(url, data, headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.post(url, data=data, headers=headers,
                      auth=HTTPBasicAuth('kakou', 'sx2767722'))

    return r
  
if __name__ == '__main__':  # pragma nocover
    #TestHttpPost()
    urlstr = 'http://127.0.0.1:8017/v1/package'
    #json_data = json.dumps(['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg'])
    data={'key':'sx2767722','urls': ['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg']}
    print json.dumps(data)
    r = send_post(urlstr, json.dumps(data))
    print r.status_code
    print r.text
