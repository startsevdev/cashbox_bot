import sys
import re
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


@bot.message_handler(commands=["revenue"])
def revenue(message):
    console_print(message)
    bot.send_message(message.from_user.id, db.revenue())


@bot.message_handler(content_types="text")
def text(message):
    console_print(message)

    search_date_result = re.search("\d{2}.\d{2}.\d{4}", message.text)
    if "выручка" in message.text.lower() and search_date_result:
        date = search_date_result.group(0)
        bot.send_message(message.from_user.id, db.revenue(date))
    elif "выручка" == message.text.lower():
        bot.send_message(message.from_user.id, db.revenue())
    elif "выручка" in message.text.lower():
        bot.send_message(message.from_user.id, "Ошибка! Неверный формат даты. Попробуй еше раз.")
    else:
        bot.send_message(message.from_user.id, db.add_sale(message.text))


bot.polling()
