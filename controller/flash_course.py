"""
    Flash-course bot runner by symmetrical-potato
    with fucking threads :)
"""

import argparse

import logging
import asyncio
import threading


from telegram.ext import Updater, Handler, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton

# from model.Courses import Courses


""" Handlers """
def on_start_command(bot, update):
    chat_id = update.message.chat_id
    #initialize number of message
    clients[chat_id] = {'red_message': True,
                        'timer' : 3}
    #first_message = md.new_user(token, chat_id)

    user_name = update.message.from_user['first_name'] + " " + update.message.from_user['last_name']
    welcome_message = 'Привет, {0}.'.format(user_name) + \
                      'Ты подписался на курс %название курса%'
                    # + db.get_description(token)
    bot.sendMessage(chat_id=chat_id, text=welcome_message)

    #bot.sendMessage(chat_id=chat_id, text=first_message)

def on_text_message(bot, update):
    chat_id = update.message.chat_id
    if update.message.text == 'Прочитал, вполне прикольно :)':
        bot.sendMessage(chat_id=chat_id, text='А ты хорош:)')
        clients[chat_id]['red_message'] = True


"""Wrappers"""
def updater_wrapper():
    updater.start_polling()

def async_loop_wrapper():
    global loop
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(send_course_message())
    finally:
        loop.close()


@asyncio.coroutine
def send_course_message():
    while True:
        asyncio.set_event_loop(loop=loop)
        if not clients: #check if empty
            yield from asyncio.sleep(1)

        for chat_id, client in clients.items():
            if client['timer'] <= 0:
                if client['red_message']:
                    message = 'lorem ipsum'
                    #timer, message =  model.get_info(token, chat_id)
                    key_board = ReplyKeyboardMarkup([['Прочитал, вполне прикольно :)']], one_time_keyboard=True)
                    updater.bot.sendMessage(chat_id=chat_id, text=message, reply_markup=key_board)

                    client['red_message'] = False
                    # model.set_read(token, chat_id)
                    # client['timer'] =
                else:
                    continue
            else:
                client['timer'] -= 3
        yield from asyncio.sleep(1)


if __name__ == '__main__':
    #variables
    clients = dict()

    #token parsing
    parser = argparse.ArgumentParser(description='Run flash-course telegram bot by your token')
    parser.add_argument('token', help='Just add token;)',
                        type=str)
    token = parser.parse_args().token

    #telegram updater
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    #handlers
    start_handler = CommandHandler('start', on_start_command)
    mesg_handler = MessageHandler([Filters.text], on_text_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mesg_handler)

    threads_targets = [updater_wrapper, async_loop_wrapper]
    for target in threads_targets:
        threading.Thread(target=target).start()

    # database init

    # model = Courses()
    # model.init_bot(token)

