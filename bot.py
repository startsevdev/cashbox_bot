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
db = Database()
parser = Parser()
csv_generator = CSVGenerator()


def keyboard():
    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    items = db.items_list()
    if len(items) % 2:
        for i in range(0, len(items) - 1, 2):
            kb.add(items[i], items[i + 1])
        kb.add(items[i + 2])
    else:
        for i in range(0, len(items), 2):
            kb.add(items[i], items[i + 1])
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
    if type(bot_message) == str or type(bot_message) == float or type(bot_message) == int:
        bot.send_message(message.from_user.id, bot_message, reply_markup=keyboard())
    else:
        bot.send_document(message.chat.id, bot_message, reply_markup=keyboard())


bot.infinity_polling(True)

