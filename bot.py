import sys
from datetime import datetime
import telebot
from db import Database
sys.path.append('../')
import tokens

bot = telebot.TeleBot(tokens.KKCashboxBot, threaded=False)
db = Database("/Users/alexander/code/bots/CashboxBot/data.db")


def console_print(message):
    now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    print("{} | {}: {}".format(now, message.from_user.id, message.text))


@bot.message_handler(content_types="text")
def text(message):
    console_print(message)
    bot.send_message(message.from_user.id, db.add_sale(message.text))


bot.polling()
