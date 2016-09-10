import sys

import logging
import asyncio

from telegram.ext import Updater, Handler, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton

import model.Courses as md

clients = dict() #?


token = '254385124:AAFzW49rQixpdUMfGpG3h2FYB049lDtBYJk'

updater = Updater(token=token)
dispatcher = updater.dispatcher


md.init_bot(token)

loop = asyncio.get_event_loop()


def on_start_command(bot, update):
    chat_id = update.message.chat_id
    #initialize number of message
    clients[chat_id] = 0


    #first_message = md.new_user(token, chat_id)

    user_name = update.message.from_user['first_name'] + " " + update.message.from_user['last_name']
    welcome_message = 'Привет, {0}.'.format(user_name) + \
                      'Ты подписался на курс %название курса%'
                    # + db.get_description(token)
    bot.sendMessage(chat_id=chat_id, text=welcome_message)

    #bot.sendMessage(chat_id=chat_id, text=first_message)

    run_loop(chat_id)



def run_loop(chat_id):
    #!check time
    #loop.call_later(1000000, send_course_message, chat_id)
    send_course_message(chat_id)



def send_course_message(chat_id):

    message = 'lorem ipsum'

    kb = ReplyKeyboardMarkup([['Прочитал, вполне прикольно :)']], one_time_keyboard=True)
    updater.bot.sendMessage(chat_id=chat_id, text=message, reply_markup=kb)

def on_text_message(bot, update):
    chat_id = update.message.chat_id

    if update.message.text == 'Прочитал, вполне прикольно :)':
        bot.sendMessage(chat_id=chat_id, text='А ты хорош:)')






print("Running main loop")
#loop.run_forever()



start_handler = CommandHandler('start', on_start_command)
mesg_handler = MessageHandler([Filters.text], on_text_message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesg_handler)



updater.start_polling()
