# -*- coding: utf-8 -*-
import os
import urllib
import datetime


class MyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UrlError(Exception):

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr('Url Error')


class HelpFunc:
    """����������"""
    def get_time(self):
        """"���ص�ǰʱ���ʽ���ַ���"""
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    def ip_to_bigint(self, ipaddr):
        """"�ַ�������IPת��������"""
        ip_strs = ipaddr.split(".")

        return str(int(ip_strs[3]) + int(ip_strs[2]) * 256 + int(ip_strs[1]) *
                   256 * 256 + int(ip_strs[0]) * 256 * 256 * 256)

    def bigint_to_ip(self, int_str):
        """"����IPת�����ַ�������"""
        bigint = int(int_str)

        first = bigint / (256 * 256 * 256)
        rest = bigint - (first * 256 * 256 * 256)

        second = rest / (256 * 256)
        rest -= second * 256 * 256

        third = rest / 256
        fourth = rest - third * 256

        return "%d.%d.%d.%d" % (first, second, third, fourth)

    def get_img_by_url(self, url, path, filename):
        """����URL��ַץͼ�������ļ��У�����str�����ļ���"""
        try:
            local = os.path.join(path, filename)
            filename, headers = urllib.urlretrieve(
                url.replace('\\', '/').encode('utf8'), local)

            return filename
        except:
            raise UrlError(url)

if __name__ == '__main__':
    hf = HelpFunc()
    print hf.getTime()
