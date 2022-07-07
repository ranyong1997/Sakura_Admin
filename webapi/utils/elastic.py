#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 14:39
# @Author  : 冉勇
# @Site    : 
# @File    : elastic.py
# @Software: PyCharm
# @desc    : elasticsearch相关
import traceback
from elasticsearch7 import AsyncElasticsearch
from webapi.setting import settings

es = AsyncElasticsearch(hosts=f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}')  # 创建es客户端
INDEX = 'posts'


async def es_search(keyword, page=1, limit=10):  # 分页查询
    """
    搜索文档
    :param keyword: 搜索关键字
    :param page: 当前页
    :param limit: 每页条数
    :return:
    """
    offset = limit * (page - 1)
    resp = await es.search(
        index=INDEX,
        query={
            "bool": {
                "should": [
                    {
                        "match": {
                            'title': keyword
                        }
                    },
                    {
                        "match": {
                            'description': keyword
                        }
                    },
                    {
                        "match": {
                            'body': keyword
                        }
                    }
                ]
            }
        },
        highlight={
            "fields": {
                "title": {},
                "description": {}
            },
            "pre_tags": '<span style="color:red;">',
            "post_tags": '</span>',
            "fragment_size": 10,
        },
        from_=offset,
        size=limit
    )
    return parse_data(resp)


def parse_data(data):
    """
    解析数据
    :param data:
    :return:
    """
    total = data['hits']['total']['value']  # 总条数
    items = []  # 文档列表
    for h in data['hits']['hits']:
        items.append({
            'id': h['_source']['id'],
            'title': h['_source']['title'],
            'description': h['_source']['description'],
            'body': h['_source']['body'],
            'timestamp': h['_source']['timestamp'],
        })
    return {
        'total': total,
        'items': items
    }


async def es_update_doc(data):  # 更新文档
    await es_create_doc(data)


async def es_delete_doc(_id):  # 删除文档
    try:
        await es.delete(
            index=INDEX,
            id=_id,
            ignore=[400, 404]
        )
    except Exception as e:
        traceback.print_exc()


async def es_create_doc(data):  # 创建文档
    try:
        await es_delete_doc(data['id'])
        await es.create(
            index=INDEX,
            id=data['id'],
            document=data,
            ignore=[400, 404]
        )
    except Exception as e:
        traceback.print_exc()
