#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course

from telegram.ext import Updater, CommandHandler, RegexHandler
import logging 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
# Reading token from external file
def getToken(): 
    import os
    from os.path import join, dirname
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    token = os.environ.get("TOKEN")
    return(token)


def start(bot, update):
    text = """
*Welcome to the Photo Store Bot.*

You can see the /gallery or know more /about this bot.
"""
    bot.send_message(chat_id=update.message.chat_id, 
                     text=text, 
                     parse_mode='Markdown')

def about(bot,update):
    text = """
*About Photo Store Bot*

The aim of this bot is to proide a simple solution for selling photos withing telegram.

You can see (by now) sample photos to be sold in /gallery.

This bot is (being) made by Mostafa Ahangarha as the project for [StartingUp2017](https://github.com/Startingup2017python2/telegramShop) course.
    """
    bot.send_message(chat_id=update.message.chat_id, 
                     text=text, 
                     parse_mode='Markdown')
    
def gallery(bot,update):
    import db
    galleryItams = db.getGalleryItems()
    
    for i in galleryItams:
        photo_id = i['id']
        title = i['title']
        url = i['url']
        filename = 'photos/'+ i['filename']
        
        command = 'Detail: /info_{} | Buy: /buy_{}'.format(photo_id, photo_id)
        
        if url is None:
            #If there is no URL, upload the photo
            logging.info('Uploading {}'.format(filename))
            with open(filename, "rb") as file:
                photo=file
        else:
            logging.info('Sending {} from url'.format(filename))
            photo=url
            
        bot.send_photo(chat_id=update.message.chat_id, 
                       photo=photo,
                       caption=title+' | '+command)

def buy(bot, update, **args):
    item_id=args['groups'][0]
    text = 'Buying the photo with id={} will be managed here...'.format(item_id)
    bot.send_message(chat_id=update.message.chat_id, 
                     text=text, 
                     parse_mode='Markdown')

def info(bot, update, **args):
    item_id=args['groups'][0]
    
    import db
    galleryItam = db.getGalleryItem(item_id)
    
    if galleryItam == None:
        logging.info('No item found in database with id={}'.format(item_id))
        text = "No Item found (or wrong item id was sent)"
    else:
        photo_id    = galleryItam['id']
        title       = galleryItam['title']
        url         = galleryItam['url']
        filename    = 'photos/'+ galleryItam['filename']
        
        if url is None:
            #If there is no URL, upload the photo
            logging.info('Uploading {}'.format(filename))
            with open(filename, "rb") as file:
                photo=file
        else:
            logging.info('Sending {} from url'.format(filename))
            photo=url
        
        
        # The following information is for presentation. Later, all of them
        # must 
        text        = """ *Title:* {}  
*By:* Mostafa Ahangarha

*Size:* 100x70 cm  
*On:* Sep 15, 2017

*Price:* $ 30

*Buy:* /buy\_{}""".format(title, photo_id)
    
        bot.send_photo(chat_id=update.message.chat_id, 
                           photo=photo)
        
        bot.send_message(chat_id=update.message.chat_id, 
                         text=text, 
                         parse_mode='Markdown')

# ///////////////////////////////////////////////

updater = Updater(getToken())
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('gallery', gallery))

# detect /buy_123 links
dispatcher.add_handler(RegexHandler(r'^/buy_(\d+)', buy, pass_groups=True))
# detect /info_123 links
dispatcher.add_handler(RegexHandler(r'^/info_(\d+)', info, pass_groups=True))

updater.start_polling()

print("The bot is running...")

updater.idle()

