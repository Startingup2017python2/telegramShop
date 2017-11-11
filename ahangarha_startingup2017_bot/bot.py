#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import logging

import userManagement as users
import orderManagement as orders

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

main_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Gallery'),
            KeyboardButton(text='About'),
        ],
    ],
    resize_keyboard=True
)


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
    global main_keyboard

    # register user id
    # Chat_id is the user's unique id
    users.registerUser(update.message.chat_id)

    text = """
*Welcome to the Photo Store Bot.*

You can see the *gallery* or know more *about* this bot.
"""
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=main_keyboard,
    )


def about(bot, update):
    text = """
*About Photo Store Bot*

The aim of this bot is to proide a simple solution for selling photos withing
 telegram.

You can see (by now) sample photos to be sold in *gallery*.

This bot is (being) made by Mostafa Ahangarha as the project for
 [StartingUp2017](https://github.com/Startingup2017python2/telegramShop)
 course."""

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode='Markdown'
    )


def gallery(bot, update):
    import db
    galleryItams = db.getGalleryItems()

    for i in galleryItams:
        photo_id = i['id']
        title = i['title']
        url = i['url']
        filename = 'photos/' + i['filename']

        if url is None:
            # If there is no URL, upload the photo
            logging.info('Uploading {}'.format(filename))
            with open(filename, "rb") as file:
                photo = file
        else:
            logging.info('Sending {} from url'.format(filename))
            photo = url

        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=photo,
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    (
                        InlineKeyboardButton(
                            text='More...',
                            callback_data="info_{}".format(photo_id)
                        )
                    )
                ]
            ]
        )

        bot.send_message(chat_id=update.message.chat_id,
                         text=title,
                         parse_mode='Markdown',
                         reply_markup=keyboard)


def buy(bot, update):
    query = update.callback_query
    data = query['data']  # Format: job_id

    item_id = data.split('_')[1]

    orders.registerOrder(query.message.chat_id, item_id)
    logging.info(
        "New order registered: User {}({}) ordered {}".format(
            query.message.chat_id,
            query.message.chat['username'],
            item_id,
        )
    )

    text = """You order for the photo with id={} is registered successfully.
 But still we cannot ship it!""".format(item_id)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          text=text,
                          parse_mode='Markdown',
                          message_id=query.message.message_id)


def info(bot, update):
    query = update.callback_query
    data = query['data']  # Format: job_id

    item_id = data.split('_')[1]

    import db
    galleryItam = db.getGalleryItem(item_id)

    keyboardBtn = []

    if galleryItam is None:
        logging.info('No item found in database with id={}'.format(item_id))
        text = "No Item found (or wrong item id was sent)"
    else:
        photo_id = galleryItam['id']

        text = """*{}*
_By: {}_

*Size:* {} cm

*Price:* {} IRR""".format(
                 galleryItam['title'],
                 galleryItam['by'],
                 galleryItam['size'],
                 galleryItam['price'],
            )
        keyboardBtn.append(
            [
                (
                    InlineKeyboardButton(
                        text='Buy',
                        callback_data="buy_{}".format(photo_id),
                    )
                ),
            ]
        )

    keyboard = InlineKeyboardMarkup(keyboardBtn)

    bot.edit_message_text(chat_id=query.message.chat_id,
                          text=text,
                          parse_mode='Markdown',
                          message_id=query.message.message_id,
                          reply_markup=keyboard)


def msgRedirect(bot, update):
    if update.message.text == 'About':
        about(bot, update)
    elif update.message.text == 'Gallery':
        gallery(bot, update)


def callbackQueryManager(bot, update):
    query = update.callback_query
    data = query['data']  # Format: job_id

    job = data.split('_')[0]
    if job == 'info':
        info(bot, update)
    elif job == 'buy':
        buy(bot, update)


# ///////////////////////////////////////////////

updater = Updater(getToken())
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('gallery', gallery))

updater.dispatcher.add_handler(CallbackQueryHandler(callbackQueryManager))

dispatcher.add_handler(MessageHandler(Filters.text, msgRedirect))
updater.start_polling()

print("The bot is running...")

updater.idle()
