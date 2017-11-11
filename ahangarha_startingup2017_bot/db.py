#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:00:54 2017

@author: sama

This file is meant to handle all database related jobs.
"""
import redis

r = redis.StrictRedis()


def getGalleryItems(start=0, count=5):
    items = []  # This array will be returned

    # Getting all the product ids
    product_id = []
    for item in r.keys('p:*'):
        p_id = item.decode('utf-8').split(':')[1]
        product_id.append(p_id)

    product_id.sort()  # sort id
    for i in product_id:
        item = {}
        item['id'] = i
        name = 'p:{}'.format(i)
        for key, value in r.hgetall(name).items():
            key = key.decode('utf-8')
            value = value.decode('utf-8')
            item[key] = value
        items.append(item)

    return(items)


def getGalleryItem(item_id=None):
    item = {}
    item['id'] = item_id
    name = 'p:{}'.format(item_id)
    for key, value in r.hgetall(name).items():
        key = key.decode('utf-8')
        value = value.decode('utf-8')
        item[key] = value

    return item


def addDefaultData():

    url_prefix = 'https://raw.githubusercontent.com/ahangarha/telegramShop/'
    url_prefix += 'master/ahangarha_startingup2017_bot/photos/'
    items = [
        {'id': '0',
         'by': 'Mostafa Ahagnarha',
         'url': url_prefix + 'ahangarha001.jpg',
         'title': 'UbuntuFest1704, Panorama',
         'filename': 'ahangarha001.jpg',
         'size': '100x70',
         'price': 500000},
        {'id': '1',
         'by': 'Mostafa Ahagnarha',
         'url': url_prefix + 'ahangarha002.jpg',
         'title': 'UbuntuFest1704, Machine Learning Presentation',
         'filename': 'ahangarha002.jpg',
         'size': '100x70',
         'price': 700000},
        {'id': '3',
         'by': 'Mostafa Ahagnarha',
         'url': url_prefix + 'ahangarha003.jpg',
         'title': 'Danial Behzadi reviews the history of Ubuntu',
         'filename': 'ahangarha003.jpg',
         'size': '100x70',
         'price': 400000},
        {'id': '4',
         'by': 'Mostafa Ahagnarha',
         'url': url_prefix + 'ahangarha004.jpg',
         'title': 'Salek explains how Wikipedia works',
         'filename': 'ahangarha004.jpg',
         'size': '100x70',
         'price': 300000},
    ]

    for item in items:
        name = 'p:{}'.format(item['id'])  # making redis name as p:<id>
        item.pop('id')  # to get other attributes than id
        for (key, value) in item.items():
            r.hset(name, key, value)


if __name__ == '__main__':
    # addDefaultData()  # uncomment this line if you want to add default data
    print('Nothing to do!')