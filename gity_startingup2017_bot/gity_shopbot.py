from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import urllib.request,io


updater=Updater('TOKEN')

def main_menu(bot,update):
    menu=[['تماس با ما','درباره ما','گروه محصولات']]

    bot.sendMessage(update.message.chat_id,"از منوی زیر بخش مورد نظر را انتخاب کنید:",reply_markup=ReplyKeyboardMarkup(menu))


def product_menu(bot,update):
    menu=[['منوی اصلی','ادکلن های مشترک','ادکلن های زنانه','ادکلن های مردانه']]

    bot.sendMessage(update.message.chat_id,"از منوی زیر بخش مورد نظر را انتخاب کنید:",reply_markup=ReplyKeyboardMarkup(menu))


def start_method(bot,update):
    bot.sendMessage(update.message.chat_id,"hellow user!!" )


def sendImage(bot,update):
    chat_id = update.message.chat_id
    url = "http://www.samatak.com/image/2016/09/2/1033807340-samatak-com.jpg";
    img =io.BytesIO(urllib.request.urlopen(url).read())
    bot.send_photo(chat_id, img, 'محصول شماره ۱: قیمت ۲۵۰۰۰۰')



updater.dispatcher.add_handler(CommandHandler('main',main_menu))
updater.dispatcher.add_handler(CommandHandler('product',product_menu))
updater.dispatcher.add_handler(CommandHandler('start',start_method))
updater.dispatcher.add_handler(CommandHandler('sendphoto',sendImage))
updater.start_polling()
updater.idle()
