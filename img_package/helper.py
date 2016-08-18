﻿# -*- coding: utf-8 -*-
import shutil

#import requests


def get_url_img(url, path, s):
    """根据URL地址抓图到本地文件"""
    r = s.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()
