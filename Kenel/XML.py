#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Waner <wanernet@qq.com>'
__all__ = ["XML"]

import xmltodict


class XML:
    def __init__(self):
        pass

    @classmethod
    def toXML(cls, json):
        """ JSON 转换成 XML
        :param json: JSON内容
        :return: 返回XML
        """
        return xmltodict.unparse(json, pretty=True)

    @classmethod
    def formXML(cls, xml, process_namespaces=False):
        """ XML 转换成 JSON
        :param xml: XML内容
        :param process_namespaces: 是否支持namespaces
        :return: 返回JSON
        """
        return xmltodict.parse(xml, process_namespaces)