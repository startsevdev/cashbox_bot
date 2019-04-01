import sys
from datetime import datetime
import telebot
from telebot import types
from db import Database
from parser import Parser
from csv_generator import CSVGenerator
import messages
sys.path.append('../')
import tokens


bot = telebot.TeleBot(tokens.CoffeeCultureBot, threaded=False)
db = Database("/Users/alexander/code/bots/CashboxBot/data.db")
parser = Parser()
csv_generator = CSVGenerator()


def keyboard():
    items = db.items_list()
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in items:
        kb.add(item)
    return kb


def console_print(message):
    now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    print("{} | {}: {}".format(now, message.from_user.id, message.text))


@bot.message_handler(commands=["start"])
def send_hello(message):
    console_print(message)
    bot.send_message(message.from_user.id, messages.hello_message, reply_markup=keyboard())


@bot.message_handler(commands=["revenue"])
def send_revenue(message):
    console_print(message)
    revenue = db.revenue()
    bot.send_message(message.from_user.id, revenue, reply_markup=keyboard())


@bot.message_handler(commands=["report"])
def send_report(message):
    console_print(message)
    csv_generator.write_csv(date=datetime.strftime(datetime.now(), "%d.%m.%Y"))
    csv_report = open('sales.txt', 'rb')
    bot.send_document(message.chat.id, csv_report, reply_markup=keyboard())


@bot.message_handler(commands=["help"])
def send_help(message):
    console_print(message)
    bot.send_message(message.from_user.id, messages.help_message, reply_markup=keyboard())


@bot.message_handler(content_types="text")
def text(message):
    console_print(message)
    bot_message = parser.parse_message(message.text)
    if bot_message:
        bot.send_message(message.from_user.id, bot_message, reply_markup=keyboard())
    else:
        csv_report = open('sales.txt', 'rb')
        bot.send_document(message.chat.id, csv_report, reply_markup=keyboard())


bot.polling()
