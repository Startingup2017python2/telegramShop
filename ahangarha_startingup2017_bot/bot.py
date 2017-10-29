#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course

from telegram.ext import Updater, CommandHandler, Filters
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
        filename = 'photos/'+ i['filename']
        
        command = 'buy: /buy_{}'.format(photo_id)
        
        logging.info('Uploading {}'.format(filename))
        
        with open(filename, "rb") as file:
            bot.send_photo(chat_id=update.message.chat_id, 
                           photo=file,
                           caption=title+' | '+command)

    
updater = Updater(getToken())
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('gallery', gallery))


updater.start_polling()

print("The bot is running...")

updater.idle()

