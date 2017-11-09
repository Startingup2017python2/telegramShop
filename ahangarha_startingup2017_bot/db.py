#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:00:54 2017

@author: sama

This file is meant to handle all database related jobs.
Data related to photos is saves as plain text here but it should later be
stored in proper database.
"""

url_prefix = 'https://raw.githubusercontent.com/ahangarha/telegramShop/'
url_prefix += 'master/ahangarha_startingup2017_bot/photos/'
items = [
    {'id': '0',
     'url': url_prefix + 'ahangarha001.jpg',
     'title': 'UbuntuFest1704, Panorama',
     'filename': 'ahangarha001.jpg'},
    {'id': '1',
     'url': url_prefix + 'ahangarha002.jpg',
     'title': 'UbuntuFest1704, Machine Learning Presentation',
     'filename': 'ahangarha002.jpg'},
    {'id': '3',
     'url': url_prefix + 'ahangarha003.jpg',
     'title': 'Danial Behzadi reviews the history of Ubuntu',
     'filename': 'ahangarha003.jpg'},
    {'id': '4',
     'url': url_prefix + 'ahangarha004.jpg',
     'title': 'Salek explains how Wikipedia works',
     'filename': 'ahangarha004.jpg'},
]


def getGalleryItems(start=0, count=5):
    # This section is a temporary data-set. Here we need to make proper query
    # and send it to another function to fetch proper data from a real
    # database (perhaps sqlite)

    global items

    return(items)


def getGalleryItem(item_id=None):
    # This section is a temporary data-set. Here we need to make proper query
    # and send it to another function to fetch proper data from a real
    # database (perhaps sqlite)
    global items

    for item in items:
        if item['id'] == item_id:
            return(item)


if __name__ == '__main__':

    galleryItams = getGalleryItems()

    for i in galleryItams:
        title = i['title']
        filename = 'photos' + i['filename']
        command = 'buy: /buy_' + i['id']
        text = '  \n'.join([title, filename, command])
        print(text)
