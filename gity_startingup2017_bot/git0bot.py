# first sprint
#displaying gallary of product(perfume) to users
#python 3.4
import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
import logging
import redis
import dotenv

####################################################################################################################
#initialize  parameters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ',level=logging.INFO)
server_r=redis.Redis()

######################################################################################################################
#data

product_women = [

    {
        "id":"1",
        "name": "lamour",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن زنانه",
        "url":"http://cologneforwomen.parsiablog.com/wp-content/uploads/sites/68/2013/11/lamour-4.jpg"

    },
    {
        "id":"2",
        "name": "ricci-ricci",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن زنانه",
        "url": "http://novinwatch.com/wp-content/uploads/2014/01/odkolon-ricci-ricci-2.jpg"

    },
    {
        "id":"3",
        "name": "flowr",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن زنانه",
        "url": "http://gemperfume.com/wp-content/uploads/2014/09/HFE-1.jpg"

    },
    {
        "id": "4",
        "name": "versace",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن زنانه",
        "url": "http://www.samatak.com/image/2016/09/2/1033807340-samatak-com.jpg"

    }

]

product_men = [

    {
        "id": "1",
        "name": "sofine",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن مردانه",
        "url":"http://blog.sofine.ir/wp-content/uploads/2015/01/05017a1.jpg"
    },
    {
        "id": "2",
        "name": "nabimages",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن مردانه",
        "url":"http://hjhjhj1245.com/nabimages/l/13950412124943300.jpg"
    },
    {
        "id": "3",
        "name": "picofile",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن مردانه",
        "url":"http://s3.picofile.com/file/8196262850/product_detailed_image_28700_41287.jpg"
    },
    {
        "id": "4",
        "name": "bolgano",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن مردانه",
        "url":"https://bolgano.com/4029-large_default/%D8%A7%D8%AF%DA%A9%D9%84%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87-%D8%B1%D8%A7%D9%84%D9%81-%D9%84%D9%88%D8%B1%D9%86-%D9%BE%D9%88%D9%84%D9%88-%D8%A8%D9%84%D9%88-ralph-lauren-polo-blue.jpg"
    }

]

product_c = [

    {
        "id": "1",
        "name": "Amouage",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن مشترک",
        "url":"http://blog.sofine.ir/wp-content/uploads/2015/01/05017a1.jpg"
    },
    {
        "id": "2",
        "name": "persianfume",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن مشترک",
        "url":"http://persianfume.ir/wp-content/uploads/2016/06/%D8%A7%D8%AF%DA%A9%D9%84%D9%86-%D8%A7%DA%AF%D9%86%D8%B1-%D9%86%D8%A7%D9%85%D8%A8%D8%B1-%D9%88%D8%A7%D9%86-%D8%B9%D9%88%D8%AF-500x500.jpg"
    },
    {
        "id": "3",
        "name": "ambre",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "ادکلن مشترک",
        "url":"https://www.zanbil.ir/image/9958?name=ambre-nue-fw.jpg&wh=400x400"
    },
    {
        "id": "4",
        "name": "davidoff",
        "cost": "پانصد هزار تومان",
        "description": "ادکلن مشترک",
        "url":"https://ershaco.com/16899-thickbox_default/%D8%B9%D8%B7%D8%B1-%D9%85%D8%B4%D8%AA%D8%B1%DA%A9-%D8%B2%D9%86%D8%A7%D9%86%D9%87-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87-%D8%AF%DB%8C%D9%88%DB%8C%D8%AF%D9%88%D9%81-%D8%A2%DA%AF%D8%A7%D8%B1-%D8%A8%D9%84%D9%86%D8%AF-%D8%A7%D8%AF%D9%88-%D9%BE%D8%B1%D9%81%DB%8C%D9%88%D9%85-davidoff-agar-blend-for-women-and-men-edp.jpg"
    }

]
##########################################################################################################################
#get token

def getToken():
    import os
    from dotenv import Dotenv
    dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    os.environ.update(dotenv)
    token = os.environ.get('TOKEN')
    return (token)


#############################################################################################################################
#main menu

def main_menu(bot, update):
    menu = [['درباره ما', 'لیست محصولات']]


    KEYBOARD_MAIN = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    message = update.message.text

    if (message == 'درباره ما'):
        bot.sendMessage(update.message.chat_id, 'فروش انوع ادکلن های مردانه و زنانه و مشترک با قیمت مناسب',reply_markup=KEYBOARD_MAIN)


    elif (message == 'لیست محصولات'):
        product_menu(bot, update)

    else:
        bot.sendMessage(update.message.chat_id, text='لطفا گروه محصول را انتخاب کنید:', reply_markup=KEYBOARD_MAIN)

#############################################################################################################################
#product menu

def product_menu(bot, update):
    keyboard = [[InlineKeyboardButton(u'\U0001F469'+'ادکلن های زنانه', callback_data='g_1'),
                 InlineKeyboardButton(u'\U0001F468'+ 'ادکلن های مردانه', callback_data='g_2'),
                 InlineKeyboardButton("ادکلن های مشترک", callback_data='g_3')],

                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('لطفا گروه محصول را انتخاب کنید:', reply_markup=reply_markup)


#################################################################################################################################
# browsing categories and  implementing main part of bot

def inlinekeyboard_B(bot, update):
    query = update.callback_query
    chat_id=query.message.chat_id
    msg_id = query.message.message_id
    user_id = query.from_user.id
    splited_query = query.data.split("_")

    type = splited_query[0]
    if len(splited_query)==2:
        index = int(splited_query[1])

    if type == 'g':
        if index == 1:
            text = 'از ادکلن های زنانه زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prw_" + str(ind)) for
                       ind, x in enumerate(product_women)]

            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
            ])

            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

        elif index == 2:
            text = 'از ادکلن های مردانه زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prm_" + str(ind)) for
                       ind, x in enumerate(product_men)]
            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
            ])
            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

        elif index == 3:
            text = 'از ادکلن های مشترک زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prc_" + str(ind)) for
                       ind, x in enumerate(product_c)]
            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
            ])
            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    elif type == 'prw':
        pro = product_women[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        pro_url=pro["url"]



        keyboard = InlineKeyboardMarkup( [[(InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_2")),(InlineKeyboardButton(text='افزودن به لیست خردید'+ u'\U00002714' , callback_data="buy_w_"+str(index)))]])

        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text='<b>نام محصول:</b>' + pro_name + '\n' + 'توضیحات:' + pro_description + '\n' + 'قیمت :' + pro_cost + '<a href="' + pro_url + '"> &#160;</a>.',
                                parse_mode=ParseMode.HTML, reply_markup=keyboard)



    elif type == 'prm':
        pro = product_men[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        pro_url = pro["url"]


        keyboard = InlineKeyboardMarkup([[(InlineKeyboardButton(text=u'\U000025C0' + 'برگشت', callback_data="menu_3")),
                                            (InlineKeyboardButton(text='افزودن به لیست خردید' + u'\U00002714',callback_data="buy_m_"+str(index)))]])

        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text='<b>نام محصول:</b>' + pro_name + '\n' + 'توضیحات:' + pro_description + '\n' + 'قیمت :' + pro_cost + '<a href="' + pro_url + '"> &#160;</a>.',
                                parse_mode=ParseMode.HTML, reply_markup=keyboard)





    elif type == 'prc':
        pro = product_c[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        pro_url = pro["url"]


        keyboard = InlineKeyboardMarkup([[(InlineKeyboardButton(text=u'\U000025C0' + 'برگشت', callback_data="menu_4")),
                                          (InlineKeyboardButton(text='افزودن به لیست خردید' + u'\U00002714',
                                                                callback_data="buy_c_"+str(index)))]])

        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text='<b>نام محصول:</b>' + pro_name + '\n' + 'توضیحات:'+ pro_description +'\n' + 'قیمت :' + pro_cost +'<a href="'+pro_url+'"> &#160;</a>.',
                                parse_mode = ParseMode.HTML, reply_markup = keyboard)

    elif type=='buy':
        type_product = splited_query[1]
        ind_buy = int(splited_query[2])
        if type_product=='c':
            pro = product_c[ind_buy]
            pro_url = pro["url"]
            redis_buy_pro(type_product, ind_buy, chat_id)

            keyboard = InlineKeyboardMarkup(
                [[(InlineKeyboardButton(text=u'\U000025C0' + 'برگشت', callback_data="menu_4"))]])

            bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text=' محصول ' + pro[
                                    'name'] + 'به سبد خرید شما اضافه شد.' + '<a href="' + pro_url + '"> &#160;</a>',
                                parse_mode=ParseMode.HTML, reply_markup=keyboard)
        if type_product=='m':
            pro = product_men[ind_buy]
            pro_url = pro["url"]
            redis_buy_pro(type_product, ind_buy, chat_id)

            keyboard = InlineKeyboardMarkup(
                [[(InlineKeyboardButton(text=u'\U000025C0' + 'برگشت', callback_data="menu_3"))]])

            bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text=' محصول ' + pro[
                                    'name'] + 'به سبد خرید شما اضافه شد.' + '<a href="' + pro_url + '"> &#160;</a>',
                                parse_mode=ParseMode.HTML, reply_markup=keyboard)
        if type_product=='w':
            pro = product_women[ind_buy]
            pro_url = pro["url"]
            redis_buy_pro(type_product, ind_buy, chat_id)

            keyboard = InlineKeyboardMarkup(
                [[(InlineKeyboardButton(text=u'\U000025C0' + 'برگشت', callback_data="menu_2"))]])

            bot.editMessageText(chat_id=user_id, message_id=msg_id,
                                text=' محصول ' + pro[
                                    'name'] + 'به سبد خرید شما اضافه شد.' + '<a href="' + pro_url + '"> &#160;</a>',
                                parse_mode=ParseMode.HTML, reply_markup=keyboard)



        #commit buy in redis


    if query.data == 'menu_2':

        text = 'از ادکلن های زنانه زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prw_" + str(ind)) for
                    ind, x in enumerate(product_women)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    if query.data == 'menu_3':
        text = 'از ادکلن های مردانه زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prm_" + str(index)) for
                    index, x in enumerate(product_men)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    if query.data == 'menu_4':
        text = 'از ادکلن های مشترک زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prc_" + str(ind3)) for
                    ind3, x in enumerate(product_c)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text=u'\U000025C0'+'برگشت', callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    elif query.data == 'menu_1':
        text ='لطفا گروه محصول را انتخاب کنید:'

        keyboard = [[InlineKeyboardButton(u'\U0001F469' + 'ادکلن های زنانه', callback_data='g_1'),
                     InlineKeyboardButton(u'\U0001F468' + 'ادکلن های مردانه', callback_data='g_2'),
                     InlineKeyboardButton("ادکلن های مشترک", callback_data='g_3')],

                    ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=reply_markup)



def redis_buy_pro(type_product,ind_buy,chat_id):
    chat_id=str(chat_id)

    key='order:'+chat_id
    PRO=type_product+'|'+str(ind_buy)
    server_r.rpush(key,PRO)
    logging.info('ordered '+type_product+' ,'+str(ind_buy)+' by user '+chat_id)

def redis_register_user(bot,update):

    chat_id=str(update.message.chat_id)
    key='user'
    server_r.set(key,update.message.chat_id)
    logging.info('registered user with ID= '+ chat_id)
    KEYBOARD_MAIN = ReplyKeyboardMarkup([
        [KeyboardButton(text='درباره ما'), KeyboardButton(text='لیست محصولات')],
    ], resize_keyboard=True)

    bot.sendMessage(update.message.chat_id,
                    text="سلام {} . به فروشگاه ما خوش آمدید. شما می توانید از دکمه لیست محصولات به لیست ادکلن های این فروشگاه دسترسی یابید. ".format(
                        update.message.chat.first_name),
                    reply_markup=KEYBOARD_MAIN)



######################################################################################################################
#add handlers


updater = Updater(getToken())
updater.dispatcher.add_handler(CommandHandler('start', redis_register_user))
updater.dispatcher.add_handler(CallbackQueryHandler(inlinekeyboard_B))
updater.dispatcher.add_handler(MessageHandler(Filters.text, main_menu))
updater.start_polling()
updater.idle()
