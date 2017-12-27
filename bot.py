from telegram.ext import Updater, CommandHandler


def start(bot, update):
    update.message.reply_text(
        'Yolo')

def saluda(bot, update):
    update.message.reply_text(
        'Hola {}'.format(update.message.from_user.first_name))
        

updater = Updater('502678844:AAHREBEvtxfckKlnfF38_dVpLXu7BsNpjy0')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('saluda', saluda))

updater.start_polling()
updater.idle()