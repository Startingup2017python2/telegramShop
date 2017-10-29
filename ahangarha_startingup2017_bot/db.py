#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:00:54 2017

@author: sama

This file is meant to handle all database related jobs.
Data related to photos is saves as plain text here but it should later be
stored in proper database.
"""

def getGalleryItems(start=0, count=5):
    # This section is a temporary data-set. Here we need to make proper query
    # and send it to another function to fetch proper data from a real
    # database (perhaps sqlite)
    
    items = []
    items.append({'id'      :'0',
                  'title'       :'UbuntuFest1704, Panorama',
                  'filename'    :'ahangarha001.jpg'})
    items.append({'id'      :'1',
                  'title'       :'UbuntuFest1704, Machine Learning Presentation',
                  'filename'    :'ahangarha002.jpg'})
#    items[2]={'title'       :'Title 3',
#              'filename'    :'ahangarha003.jpg'}
#    items[3]={'title'       :'Title 4',
#              'filename'    :'ahangarha004.jpg'}
    
    return(items)

if __name__ == '__main__':
    
    galleryItams = getGalleryItems()
    
    for i in galleryItams:
        title = i['title']
        filename = 'photos'+ i['filename']
        command = 'buy: /buy_' + i['id']
        text = '  \n'.join([title, filename, command])
        print(text)