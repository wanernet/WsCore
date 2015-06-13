#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        # print ('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = attrs.get('__primary_key__', None) or None
        for k, v in attrs.items():
            from db.Field import Field

            if isinstance(v, Field):
                # print ('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if primary_key:
                    fields.append(k)
                else:
                    if v.primary_key:
                        # if primary_key:
                        #     raise StandardError('Duplicate primary key for field: %s' % k)
                        primary_key = k
                    else:
                        fields.append(k)
        if not primary_key:
            raise StandardError('Primary key not found.')
        for key in mappings.keys():
            attrs.pop(key)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        # assert isinstance(table_name, object)
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        return type.__new__(mcs, name, bases, attrs)
