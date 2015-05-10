# -*- coding: utf-8 -*-
import shutil

import requests


class RequestsFunc:
    """HTTP客服端类"""
    def get_url_img(self, url, path):
        """根据URL地址抓图到本地文件"""
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        # 非200响应,抛出异常
        r.raise_for_status()

    def send_post(self, url, send_data):
        """POST请求"""
        r = requests.post(url, data=send_data, headers={'Content-Type': 'application/json'})

        return r

if __name__ == '__main__':
    import json
    rf = RequestsFunc()
    url = 'http://127.0.0.1:8017/v1/package'
    #data = {'key': 'sx2767722', 'id': 1}
    urls = ['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg']
    data = {'key':'sx2767722','urls': urls}
    r = rf.send_post(url, json.dumps(data))
    print r.status_code
    print r.text
    #print rf.send_post(url, data)
