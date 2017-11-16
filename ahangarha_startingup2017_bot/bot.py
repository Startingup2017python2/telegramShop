#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mostafa Ahangarha
# Licence: GPLv3
# Description: This is homework for StartingUp2017 course

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import db
import logging

import userManagement as users
import orderManagement as orders


def is_admin(user_id):
    if user_id == getEnvVar('ADMIN_ID'):
        return True
    else:
        return False


# Reading token from external file
def getEnvVar(varName):
    import os
    from os.path import join, dirname
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    result = os.environ.get(varName)
    return(result)


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
    galleryItams = db.getGalleryItems()

    for i in galleryItams:

        bot.send_photo(
            chat_id=update.message.chat_id,
            photo=i['file_id'],
        )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    (
                        InlineKeyboardButton(
                            text='More...',
                            callback_data="info_{}".format(i['id'])
                        )
                    )
                ]
            ]
        )

        bot.send_message(chat_id=update.message.chat_id,
                         text=i['title'],
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

    product_id = data.split('_')[1]

    text = productDetails(product_id)

    keyboardBtn = []
    keyboardBtn.append(
        [
            (
                InlineKeyboardButton(
                    text='Buy',
                    callback_data="buy_{}".format(product_id),
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


def productDetails(product_id):
    product = db.getGalleryItem(product_id)
    product.pop('file_id')
    product.pop('id')
    text = ''
    if product['title'] is not None:
        text += "*{}*\n".format(product['title'])
        product.pop('title')
    if product['price'] is not None:
        text += "Price: {}\n".format(product['price'])
        product.pop('price')
    text += '_' * 20 + "\n"
    for key, value in product.items():
        text += "{}: {}\n".format(key.capitalize(), value)

    return text


def msgRedirect(bot, update):
    if update.message.text == 'About':
        about(bot, update)
    elif update.message.text == 'Gallery':
        gallery(bot, update)


def uploadPhoto(bot, update):
    keyValues = {}  # dictionary containing key-values to be saved in db
    # There are three versions of the uploaded photos. photo[0] is the lightest
    # and the photo [2] is the largest in terms of size. Since we don't need
    # large files we will only save the light version. Otherwise we need to
    # save all the files_ids in an array
    file_id = update.message.photo[0].file_id
    caption = update.message.caption
    # caption structure is as key1:val1\nkey2:val2\n...
    keyValues['file_id'] = file_id

    rows = caption.split('\n')
    for row in rows:
        key, value = row.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        keyValues[key] = value

    # TODO: Make sure the necessary data (title and price) are provided
    product_id = db.add_new_item(keyValues)

    if product_id is False:
        text = "Not successfull! :("
    else:
        text = "Added successfully :)\n\nInto:\n"
        text += productDetails(product_id)

    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=db.getGalleryItem(product_id)['file_id']
    )

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        parse_mode='Markdown',
    )
    # Send a post to registered users and norify them about the new product
    notifyUsers(bot, update, product_id)


def notifyUsers(bot, update, product_id):
    photo = db.getGalleryItem(product_id)['file_id']
    # get all users id from db
    user_ids = users.getAllUsersId()
    #   notify each user
    for user_id in user_ids:
        logging.info("Sending notification to {}".format(user_id))

        # Avoid sending notification to the admin
        if is_admin(user_id):
            continue
        bot.send_message(
            chat_id=user_id,
            text="There is a new item in our Store:",
        )

        bot.send_photo(
            chat_id=user_id,
            photo=photo
        )

        text = productDetails(product_id)

        bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode='Markdown',
        )


def callbackQueryManager(bot, update):
    query = update.callback_query
    data = query['data']  # Format: job_id

    job = data.split('_')[0]
    if job == 'info':
        info(bot, update)
    elif job == 'buy':
        buy(bot, update)


def temp(bot, update):
    print(update)

# ///////////////////////////////////////////////


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

updater = Updater(getEnvVar('TOKEN'))
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('gallery', gallery))
dispatcher.add_handler(CommandHandler('temp', temp))


updater.dispatcher.add_handler(CallbackQueryHandler(callbackQueryManager))

dispatcher.add_handler(MessageHandler(Filters.text, msgRedirect))
dispatcher.add_handler(MessageHandler(Filters.photo, uploadPhoto))
updater.start_polling()

print("The bot is running...")

updater.idle()
