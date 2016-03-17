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
        'http://localhost/imgareaselect/imgs/1.jpg',
        'http://localhost/imgareaselect/imgs/2.jpg',
        'http://localhost/imgareaselect/imgs/1.jpg'
    ]
    dl = Downloader()
    dl.main(url_list)
    del dl

if __name__ == "__main__":
##    url_list = [
##        'http://localhost/imgareaselect/imgs/1.jpg',
##        'http://localhost/imgareaselect/imgs/2.jpg',
##        'http://localhost/imgareaselect/imgs/1.jpg'
##    ]
##    fetch_imgs(url_list)
    #show_path()
    test_downloader()
