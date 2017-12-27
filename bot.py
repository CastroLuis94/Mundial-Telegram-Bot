import telegram
from telegram.ext import *


mi_bot = telegram.Bot(token='502678844:AAHREBEvtxfckKlnfF38_dVpLXu7BsNpjy0')
mi_bot_updater = Updater(mi_bot.token)


def start(bot,updater,pass_chat_date = True):
    updater.message.chat_id
    bot.sendMessage(chat_id=updater.message.chat_id,text="Yolo")

start_handler = CommandHandler('start',start)

dispatcher = mi_bot_updater.dispatcher

dispatcher.add_handler(start_handler)

mi_bot_updater.start_polling()
mi_bot_updater.start_idle()

while True:
    pass