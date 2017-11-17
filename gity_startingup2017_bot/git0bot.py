# first sprint / displaying gallary of product(perfume) to users / python 3.4


from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler,\
    CallbackQueryHandler, Filters, MessageHandler,\
    ConversationHandler
import logging
import redis

# initialize  parameters


logging.basicConfig(format='%(asctime)s -'
                           ' %(name)s -'
                           ' %(levelname)s -'
                           ' %(message)s ',
                    level=logging.INFO)
server_r = redis.Redis(decode_responses=True)

# server_r.delete('order6')


print(server_r.get('idp'))
if not server_r.exists('idp'):
    server_r.set('idp', 0)
idp = 0
count = 0
NAME, PRICE, DISCRIBE, URL = range(4)
keyboard_main2 = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='افزودن محصول'),
            KeyboardButton(text='برگشت')
        ]
    ], resize_keyboard=True)

# get envvar


def get_env(var):
    import os
    from dotenv import Dotenv
    dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    os.environ.update(dotenv)
    gvar = var
    env_var = os.environ. get(gvar)

    return env_var

# main menu


def main_menu(bot, update):
    menu = [['درباره ما', 'لیست محصولات']]
    keyboard_main1 = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    global keyboard_main2
    message = update.message.text
    if message == 'درباره ما':
        bot.sendMessage(update.message.chat_id,
                        'فروش انوع ادکلن های مردانه و '
                        'زنانه و مشترک با قیمت مناسب',
                        reply_markup=keyboard_main1)
    if message == 'لیست محصولات':
        products(bot, update)

    if message == 'افزودن محصول':
        update.message.reply_text('لطفانام مربوط به محصول '
                                  'مورد نظر را وارد کنید.'
                                  'در صورت تمایل به انصراف از عملیات '
                                  '/cancel را وارد کنید:',
                                  reply_markup=keyboard_main2)
        return NAME

    if message == 'برگشت':
        bot.sendMessage(update.message.chat_id,
                        'فروش انوع ادکلن های مردانه و '
                        'زنانه و مشترک با قیمت مناسب',
                        reply_markup=keyboard_main1)

# product menu


def products(bot, update):

    for i in range(int(server_r.get('idp'))):
        if server_r.exists('order' + str(update.message.chat_id) + str(i)):
            count_buy = server_r.hget('order' +
                                      str(update.message.chat_id),
                                      str(i))
        else:
            count_buy = 0

        pro_name = server_r.hget('p' + str(i), 'name')
        pro_description = server_r.hget('p' + str(i), 'price')
        pro_cost = server_r.hget('p' + str(i), 'discribe')
        pro_url = server_r.hget('p' + str(i), 'url')
        indp = i
        keyboard = InlineKeyboardMarkup(
            [
                [
                    (
                        InlineKeyboardButton(
                            text=u'\U0000274E' + 'کاهش تعداد خریداری شده',
                            callback_data="dec_" + str(indp))),
                    (
                        InlineKeyboardButton(text='تعداد خریداری شده:' +
                                                  str(count_buy) +
                                                  u'\U00002714',
                                             callback_data="buy_" +
                                                           str(indp)
                                             )
                    )
                ]
            ]
        )
        bot.sendMessage(update.message.chat_id,
                        text='<b>نام محصول:</b>' +
                             pro_name + '\n' + 'توضیحات:' +
                             pro_description + '\n' + 'قیمت :' +
                             pro_cost + '<a href="' +
                             pro_url + '"> &#160;</a>.',
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard)


def redis_register_user(bot, update):
    chat_id = str(update.message.chat_id)
    key = 'user'
    server_r.set(key, update.message.chat_id)
    logging.info('registered user with ID= ' + chat_id)
    keyboard_main = ReplyKeyboardMarkup([
        [KeyboardButton(text='درباره ما'),
         KeyboardButton(text='لیست محصولات')]],
        resize_keyboard=True)
    bot.sendMessage(update.message.chat_id, text="سلام {}."
                                                 "به فروشگاه ما خوش آمدید."
                                                 "شما می توانید از دکمه لیست "
                                                 "محصولات به لیست ادکلن های "
                                                 "این فروشگاه دسترسی یابید."
                    .format(update.message.chat.first_name),
                    reply_markup=keyboard_main)


def login_admin(bot, update):
    global isadmin
    global keyboard_main2
    admin_id = get_env('ADMIN_ID')
    if admin_id == str(update.message.chat_id):
        update.message.reply_text(text="سلام ادمین محترم {} ."
                                       "لطفا عملیات مورد نظر "
                                       "رااز منوی زیر انتخاب کنید:"
                                  .format(update.message.chat.first_name),
                                  reply_markup=keyboard_main2)


def inlinekeyboard_b(bot, update):

    query = update.callback_query
    chat_id = query.message.chat_id
    msg_id = query.message.message_id
    user_id = query.from_user. id
    splited_query = query.data.split("_")
    typee = splited_query[0]
    index = splited_query[1]

    if typee == 'buy':

        ind_buy = index
        name_buy = server_r.hget('p' + str(ind_buy), 'name')
        pro_url = server_r.hget('p' + str(ind_buy), 'url')
        redis_buy_pro(ind_buy, chat_id)
        count_buy = server_r.hget('order' + str(chat_id), str(ind_buy))
        keyboard = InlineKeyboardMarkup(
            [
                [
                    (
                        InlineKeyboardButton(
                            text=u'\U0000274E' + 'کاهش تعداد خریداری شده',
                            callback_data="dec_" + str(ind_buy))),
                    (
                        InlineKeyboardButton(text='تعداد خریداری شده:' +
                                                  str(count_buy) +
                                                  u'\U00002714',
                                             callback_data="buy_" +
                                                           str(ind_buy)
                                             )
                    )
                ]
            ]
        )
        bot.editMessageText(chat_id=user_id,
                            message_id=msg_id,
                            text=' محصول ' +
                                 name_buy + 'به سبد خرید شما اضافه شد.' +
                                 '<a href=''"' +
                                 pro_url + '"> &#160;</a>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard)

    elif typee == 'dec':
        ind_buy = index
        if server_r.exists('order' + str(chat_id) + str(ind_buy)):

            count_buy = server_r.hget('order' + str(chat_id), str(ind_buy))
            count_buy = int(count_buy)
            if count_buy == 0:
                pass
            else:
                count_buy = count_buy - 1
                server_r.hset('order' +
                              str(chat_id),
                              str(ind_buy),
                              str(count_buy))

        name_buy = server_r.hget('p' +
                                 str(ind_buy), 'name')
        pro_url = server_r.hget('p' +
                                str(ind_buy), 'url')
        keyboard = InlineKeyboardMarkup(
            [
                [
                    (
                        InlineKeyboardButton(
                            text=u'\U0000274E' + 'کاهش تعداد خریداری شده',
                            callback_data="dec_" + str(ind_buy))),
                    (
                        InlineKeyboardButton(
                            text='تعداد خریداری شده:' +
                                 str(count_buy) +
                                 u'\U00002714',
                            callback_data="buy_" +
                                          str(ind_buy)
                        )
                    )
                ]
            ]
        )
        bot.editMessageText(chat_id=user_id,
                            message_id=msg_id,
                            text=' محصول ' +
                                 name_buy +
                                 'به سبد خرید شما اضافه شد.' +
                                 '<a href=''"' +
                                 pro_url + '"> &#160;</a>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=keyboard)

    if query.data == 'menu_1':
        main_menu()


def register_user(bot, update):

    chat_id = str(update.message.chat_id)
    key = 'user:'
    server_r.set(key + chat_id, '1')
    logging.info('registered user with ID= ' + chat_id)


def redis_buy_pro(ind_buy, chat_id):

    chat_id = str(chat_id)
    key = 'order' + chat_id
    pro = str(ind_buy)
    if server_r.exists(key + pro):
        count = int(server_r.hget(key, pro))
        server_r.hset(key, pro, str(count + 1))
    else:
        count = '1'
        server_r.hset(key, pro, count)

    server_r.set('order' + chat_id + pro, '1')
    logging.info('order:' +
                 pro + ' by user ' +
                 chat_id)


def name_p(bot, update):
    global keyboard_main2
    global idp
    update.message.reply_text('لطفا قیمت مربوط به محصول'
                              ' مورد نظر را وارد کنید.'
                              'در صورت تمایل به انصراف از عملیات '
                              '/cancel را وارد کنید:',
                              reply_markup=keyboard_main2)
    idp = server_r.get('idp')
    idp = int(idp)
    server_r.hset('p' + str(idp), 'name', update.message.text)
    idu = int(idp) + 1
    server_r.set('idp', idu)

    return PRICE


def price_p(bot, update):
    global keyboard_main2
    global idp
    update.message.reply_text('لطفا توضیحات مربوط به محصول'
                              ' مورد نظر را وارد کنید.'
                              'در صورت تمایل به انصراف از عملیات'
                              ' /cancel را وارد کنید:',
                              reply_markup=keyboard_main2)
    server_r.hset('p' + str(idp), 'price', update.message.text)

    return DISCRIBE


def discribe_p(bot, update):
    global keyboard_main2
    global idp
    update.message.reply_text('لطفا URL تصویر محصول مورد نظر را وارد کنید.'
                              'در صورت تمایل به انصراف از عملیات'
                              ' /cancel را وارد کنید:',
                              reply_markup=keyboard_main2)
    server_r.hset('p' + str(idp),
                  'discribe', update.message.text)

    return URL


def url_p(bot, update):
    global keyboard_main2
    global idp
    update.message.reply_text('اطلاعات مورد نیاز برای '
                              'ذخیره سازی داده تکمیل شد',
                              reply_markup=keyboard_main2)
    server_r.hset('p' + str(idp), 'url', update.message.text)
    pro_name = server_r.hget('p' + str(idp), 'name')
    pro_description = server_r.hget('p' + str(idp), 'price')
    pro_cost = server_r.hget('p' + str(idp), 'discribe')
    pro_url = server_r.hget('p' + str(idp), 'url')
    keyboard = InlineKeyboardMarkup(
        [
            [
                (
                    InlineKeyboardButton(
                        text=u'\U0000274E' + 'کاهش تعداد خریداری شده',
                        callback_data="dec_" + str(idp))),
                (
                    InlineKeyboardButton(text='تعداد خریداری شده:' + str(0) +
                                              u'\U00002714',
                                         callback_data="buy_" +
                                                       str(idp)
                                         )
                )
            ]
        ]
    )

    users = server_r.keys('user:*')
    for i in range(len(users)):
        users[i] = users[i].split(':')[1]
        bot.sendMessage(users[i],
                        text='<b>نام محصول:</b>' +
                             pro_name + '\n' + 'توضیحات:' +
                             pro_description + '\n' + 'قیمت :' +
                             pro_cost + '<a href="' +
                             pro_url + '"> &#160;</a>.',
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard)

    print(server_r.hget('p' + str(idp), 'name'))
    print(server_r.hget('p' + str(idp), 'price'))
    print(server_r.hget('p' + str(idp), 'discribe'))
    print(server_r.hget('p' + str(idp), 'url'))

    return ConversationHandler.END


def cancel(bot, update):

    global keyboard_main2
    update.message.reply_text('عملیات مورد نظر لغو شد',
                              reply_markup=keyboard_main2)
    return ConversationHandler.END


def main():

    updater = Updater(get_env('TOKEN'))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, main_menu)],
        states={
            NAME: [MessageHandler(Filters.text, name_p)],
            PRICE: [MessageHandler(Filters.text, price_p)],
            DISCRIBE: [MessageHandler(Filters.text, discribe_p)],
            URL: [MessageHandler(Filters.text, url_p)]},
        fallbacks=[CommandHandler('cancel', cancel)])

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('start', register_user))
    updater.dispatcher.add_handler(CommandHandler('admin', login_admin))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, main_menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(inlinekeyboard_b))
    updater.start_polling()
    updater.idle()
# add handlers


if __name__ == '__main__':
    main()
