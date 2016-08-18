import os

from gevent import monkey
import gevent
import requests

from img_package.helper import get_url_img
from img_package.downloader import Downloader

path = u'imgs'

def fetch_imgs(url_list):
    join_list = []
    count = 1
    for url in url_list:
        join_list.append(gevent.spawn(
            get_url_img, url, os.path.join(path, '%s.jpg' % count)))
        count += 1
    gevent.joinall(join_list)

def show_path():
    if os.path.isdir(path):
        print 'done'
    for d in os.listdir(path):
        print d


def test_downloader():
    url_list = [
        'http://10.44.192.70/SpreadDataH/ImageFile/2016/08/17/21/441305000004/21570700041.jpg',
        'http://10.44.192.70/SpreadDataH/ImageFile/2016/08/17/21/441305000005/21565900040.jpg',
        'http://10.44.192.67:8088/05/vhipict/201608/17/21/100000002005-20160817215652-4-1.jpg',
	'http://10.44.192.67:8088/02/vhipict/201608/17/21/100000001902-20160817215653-5-1.jpg'
    ]
    dl = Downloader()
    dl.main(url_list)
    del dl

if __name__ == "__main__":
    test_downloader()
