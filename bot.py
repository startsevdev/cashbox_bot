import sys
from datetime import datetime
import telebot
from db import Database
from parser import Parser
sys.path.append('../')
import tokens


bot = telebot.TeleBot(tokens.KKCashboxBot, threaded=False)
db = Database("/Users/alexander/code/bots/CashboxBot/data.db")
parser = Parser()


def console_print(message):
    now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    print("{} | {}: {}".format(now, message.from_user.id, message.text))


@bot.message_handler(commands=["revenue"])
def revenue(message):
    console_print(message)
    bot.send_message(message.from_user.id, db.revenue())


@bot.message_handler(content_types="text")
def text(message):
    console_print(message)
    bot_message = parser.parse_message(message.text)
    if bot_message:
        bot.send_message(message.from_user.id, bot_message)
    else:
        report_csv = open('sales.txt', 'rb')
        bot.send_document(message.chat.id, report_csv)


bot.polling()
