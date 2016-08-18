# -*- coding: utf-8 -*-
import time
import json
import shutil

from gevent import monkey
import gevent
import requests

def get_url_img(url, path):
    """根据URL地址抓图到本地文件"""
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()

def get_imgs():
    gevent.joinall([
        gevent.spawn(get_url_img, 'http://localhost/imgareaselect/imgs/1.jpg', '1.jpg'),
        gevent.spawn(get_url_img, 'http://localhost/imgareaselect/imgs/2.jpg', '2.jpg'),
        gevent.spawn(get_url_img, 'http://localhost/imgareaselect/imgs/2.jpg', '3.jpg')
    ])
    time.sleep(10)

  
if __name__ == '__main__':  # pragma nocover
    #get_url_img('http://localhost/imgareaselect/imgs/1.jpg', '1.jpg')
    get_imgs()
    print 'done'
