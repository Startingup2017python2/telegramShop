import io
import urllib

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler

updater = Updater('465765170:AAGx1PPex1-kYZ3DJ_REZMk_oh-1EWSwSMo')

product_women = [

    {
        "name": "1",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "http://www.samatak.com/image/2016/09/2/1033807340-samatak-com.jpg",

    },
    {
        "name": "2",
        "cost": "پانصد هزار تومان",
        "description": "",

    },
    {
        "name": "3",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "",

    },
    {
        "name": "4",
        "cost": "پانصد هزار تومان",
        "description": "",

    }

]

product_men = [

    {
        "name": "5",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "",
    },
    {
        "name": "6",
        "cost": "پانصد هزار تومان",
        "description": "",
    },
    {
        "name": "7",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "",
    },
    {
        "name": "8",
        "cost": "پانصد هزار تومان",
        "description": "",
    }

]

product_c = [

    {
        "name": "11",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "",

    },
    {
        "name": "22",
        "cost": "پانصد هزار تومان",
        "description": "",
    },
    {
        "name": "33",
        "cost": "از دویست هزار تومان تا چهار صد و پنجاه هزار تومان",
        "description": "",
    },
    {
        "name": "44",
        "cost": "پانصد هزار تومان",
        "description": "",
    }

]


def main_menu(bot, update):
    menu = [['درباره ما', 'لیست محصولات']]

    # bot.sendMessage(update.message.chat_id,"از منوی زیر بخش مورد نظر را انتخاب کنید:",reply_markup=ReplyKeyboardMarkup(menu))
    KEYBOARD_MAIN = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    message = update.message.text
    if (message == 'درباره ما'):
        bot.sendMessage(update.message.chat_id, 'فروش انوع ادکلن های مردانه و زنانه و مشترک با قیمت مناسب',reply_markup=KEYBOARD_MAIN)


    elif (message == 'لیست محصولات'):
        product_menu(bot, update)

    else:
        bot.sendMessage(update.message.chat_id, text='لطفا گروه محصول را انتخاب کنید:', reply_markup=KEYBOARD_MAIN)


def product_menu(bot, update):
    keyboard = [[InlineKeyboardButton("ادکلن های زنانه", callback_data='g_1'),
                 InlineKeyboardButton("ادکلن های مردانه", callback_data='g_2'),
                 InlineKeyboardButton("ادکلن های مشترک", callback_data='g_3')],

                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('لطفا گروه محصول را انتخاب کنید:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    msg_id = query.message.message_id
    user_id = query.from_user.id
    splited_query = query.data.split("_")
    type = splited_query[0]
    index = int(splited_query[1])

    if type == 'g':
        if index == 1:
            text = 'از ادکلن های زنانه زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prw_" + str(ind)) for
                       ind, x in enumerate(product_women)]

            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text="<-", callback_data="menu_1")]
            ])

            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

        elif index == 2:
            text = 'از ادکلن های مردانه زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prm_" + str(ind)) for
                       ind, x in enumerate(product_men)]
            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text="<-", callback_data="menu_1")]
            ])
            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

        elif index == 3:
            text = 'از ادکلن های مشترک زیر انتخاب کنید:'
            buttons = [InlineKeyboardButton(text=x["name"], callback_data="prc_" + str(ind)) for
                       ind, x in enumerate(product_c)]
            keyboard = InlineKeyboardMarkup([
                buttons[0:2],
                buttons[2:4],

                [InlineKeyboardButton(text="<-", callback_data="menu_1")]
            ])
            bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    elif type == 'prw':
        pro = product_women[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        #pro_url=pro["url"]

        keyboard=InlineKeyboardMarkup([[(InlineKeyboardButton(text='<-', callback_data="menu_2"))]])



        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                           text=pro_name + '\n' + pro_description + '\n' + pro_cost, reply_markup=keyboard)

    elif type == 'prm':
        pro = product_women[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        keyboard = InlineKeyboardMarkup([[(InlineKeyboardButton(text='<-', callback_data="menu_3"))]])

        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                            text=pro_name + '\n' + pro_description + '\n' + pro_cost, reply_markup=keyboard)



    elif type == 'prc':
        pro = product_women[index]
        pro_name = pro["name"]
        pro_description = pro["description"]
        pro_cost = pro["cost"]
        keyboard = InlineKeyboardMarkup([[(InlineKeyboardButton(text='<-', callback_data="menu_4"))]])

        bot.editMessageText(chat_id=user_id, message_id=msg_id,
                            text=pro_name + '\n' + pro_description + '\n' + pro_cost, reply_markup=keyboard)

    if query.data == 'menu_2':

        text = 'از ادکلن های زنانه زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prw_" + str(ind)) for
                    ind, x in enumerate(product_women)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text="<-", callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    if query.data == 'menu_3':
        text = 'از ادکلن های مردانه زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prm_" + str(index)) for
                    index, x in enumerate(product_men)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text="<-", callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    if query.data == 'menu_4':
        text = 'از ادکلن های مشترک زیر انتخاب کنید: '
        buttons = [InlineKeyboardButton(text=x["name"], callback_data="prc_" + str(index)) for
                    index, x in enumerate(product_c)]
        keyboard = InlineKeyboardMarkup([
            buttons[0:2],
            buttons[2:4],

            [InlineKeyboardButton(text="<-", callback_data="menu_1")]
        ])
        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=keyboard)

    elif query.data == 'menu_1':
        text ='لطفا گروه محصول را انتخاب کنید:'

        keyboard = [[InlineKeyboardButton("ادکلن های زنانه", callback_data='g_1'),
                     InlineKeyboardButton("ادکلن های مردانه", callback_data='g_2'),
                     InlineKeyboardButton("ادکلن های مشترک", callback_data='g_3')],

                    ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.editMessageText(chat_id=user_id, message_id=msg_id, text=text, reply_markup=reply_markup)


def start_method(bot, update):
    KEYBOARD_MAIN = ReplyKeyboardMarkup([
        [KeyboardButton(text='درباره ما'), KeyboardButton(text='لیست محصولات')],
    ], resize_keyboard=True)

    bot.sendMessage(update.message.chat_id,
                    text="سلام {} . به فروشگاه ما خوش آمدید. شما می توانید از دکمه لیست محصولات به لیست ادکلن های این فروشگاه دسترسی یابید. ".format(update.message.chat.first_name),
                    reply_markup=KEYBOARD_MAIN)
    # product_menu(bot,update)


def sendImage(bot, update):
    chat_id = update.message.chat_id
    url = "http://www.samatak.com/image/2016/09/2/1033807340-samatak-com.jpg";
    img = io.BytesIO(urllib.request.urlopen(url).read())
    bot.send_photo(chat_id, img, 'محصول شماره ۱: قیمت ۲۵۰۰۰۰')


updater.dispatcher.add_handler(CommandHandler('main', main_menu))
#updater.dispatcher.add_handler(CommandHandler('product', product_menu))
updater.dispatcher.add_handler(CommandHandler('start', start_method))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.text, main_menu))
#updater.dispatcher.add_handler(CommandHandler('sendphoto', sendImage))
updater.start_polling()
updater.idle()
