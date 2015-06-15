#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Waner <wanernet@qq.com>'
__all__ = ["IO"]

import os
import codecs

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class IO:
    def __init__(self):
        pass

    @classmethod
    def read(cls, file_path, encoding="UTF-8"):
        content = None
        if os.path.isfile(file_path):
            with codecs.open(file_path, mode='r', encoding=encoding) as f:
                content = f.read()

        return content

    @classmethod
    def remove(cls, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    @classmethod
    def write(cls, file_path, content, encoding="UTF-8"):
        if os.path.isfile(file_path):
            with codecs.open(file_path, mode='w+', encoding=encoding) as f:
                f.writelines(content)

    @classmethod
    def write_line(cls, file_path, content, encoding="UTF-8"):
        if os.path.isfile(file_path):
            with codecs.open(file_path, mode='a', encoding=encoding) as f:
                f.write(content)

    @classmethod
    def remove_dir(cls, path):
        if os.path.isdir(path):
            os.rmdir(path)

    @classmethod
    def create_dir(cls, path):
        if not os.path.isdir(path):
            os.mkdir(path)


if __name__ == "__main__":
    # BASE_DIR = os.path.dirname(__file__)
    # file_path = os.path.join(BASE_DIR, 'log.txt')
    # dir_path = os.path.join(BASE_DIR, 'log')
    # IO.create_dir(dir_path)
    # IO.remove_dir(dir_path)
    # FileHelper.remove(file_path)
    # FileHelper.write_line('log.txt', "\n this is tow test")
    # txt = FileHelper.read(file_path)
    # print txt
    # FileHelper.write('log.txt', "this is test")
    # print os.path.abspath('.')
    # print sys.path[0]
    # # print os.path.
    # # print os.path
    # file_path = "/txt/"
    # print os.path.join(sys.path[0], "/txt/aa.txt")
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 获取当前文件夹的父目录绝对路径
    # print BASE_DIR
    # file_path = os.path.join(BASE_DIR, 'txt/aa/', 'a.txt')
    # print file_path
    # # print os.getcwd()
    # import logging
    #
    # logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG)
    # logging.debug('this is a message')
    pass
