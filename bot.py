import sys
from datetime import datetime
import telebot
from telebot import types
from db import Database
from parser import Parser
from csv_generator import CSVGenerator
import messages


bot = telebot.TeleBot("891562236:AAGSXMXUxN1gYlWVtlSisGCFRIsAIytBFtg", threaded=False)
db = Database("/home/startsevdev/ccbot/data.db")
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
def start(message):
    console_print(message)
    bot.send_message(message.from_user.id, messages.hello_message, reply_markup=keyboard())


@bot.message_handler(commands=["revenue"])
def revenue(message):
    console_print(message)
    bot.send_message(message.from_user.id, db.revenue(), reply_markup=keyboard())


@bot.message_handler(commands=["report"])
def report(message):
    console_print(message)
    csv_generator.write_csv(date=datetime.strftime(datetime.now(), "%d.%m.%Y"))
    report_csv = open('sales.txt', 'rb')
    bot.send_document(message.chat.id, report_csv, reply_markup=keyboard())


@bot.message_handler(commands=["help"])
def help(message):
    console_print(message)
    bot.send_message(message.from_user.id, messages.help_message, reply_markup=keyboard())


@bot.message_handler(content_types="text")
def text(message):
    console_print(message)
    bot_message = parser.parse_message(message.text)
    if bot_message:
        bot.send_message(message.from_user.id, bot_message, reply_markup=keyboard())
    else:
        report_csv = open('sales.txt', 'rb')
        bot.send_document(message.chat.id, report_csv, reply_markup=keyboard())


bot.infinity_polling(True)
