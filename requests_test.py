# -*- coding: gbk -*-

import json
import requests
import shutil

url = 'http://g.hiphotos.baidu.com/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=49d8589cc9fcc3cea0cdc161f32cbded/d01373f082025aafaac7aa75faedab64024f1a92.jpg'
url2 = 'http://g.hiphotos.baidu.com/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign=49d8589cc9fcc3cea0cdc161f32cbded/d01373f082025aafaac7aa75faedab64024f1a931.jpg'
url4 = 'http://localhost/imgareaselect/imgs/1.jpg'
url3 = 'http://localhost/imgareaselect/imgs/马刺/1.jpg'

##r = requests.get(url3.decode('gbk').encode('utf8'), stream=True)
##path = 'c:/imgdownload/test.jpg'
##print r.status_code
##if r.status_code == 200:
##    with open(path, 'wb') as f:
##        r.raw.decode_content = True
##        shutil.copyfileobj(r.raw, f) 
 
url = 'http://127.0.0.1:8060/upload'
files = {'file': open('test2.jpg', 'rb')}
info = {'passtime':'2015-02-14 21:32:12'}
payload = {'info':json.dumps(info)}
#files = {'file': ('report.jpg', open('/home/lyb/sjzl.mpg', 'rb'))}     #显式的设置文件名

r = requests.post(url, data=payload, files=files)
print(r.text)
