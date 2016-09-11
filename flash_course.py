"""
    Flash-course bot runner by symmetrical-potato
    with fucking threads :)
"""

import argparse

import asyncio
import threading


from telegram.ext import Updater, Handler, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from model.Courses import Courses

""" Handlers """
def on_start_command(bot, update):
    chat_id = update.message.chat_id
    # print('>>',chat_id, token)
    timer, first_message = md.new_user(token, chat_id)
    # print('>>',timer, first_message)
    clients[chat_id] = {'red_message': True,
                        'timer': timer,
                        'passed': 0}

    user_name = update.message.from_user['first_name'] + " " + update.message.from_user['last_name']
    welcome_message = 'Привет, {0}.'.format(user_name) + \
                      'Ты подписался на курс {0}.'.format(md.get_description_name(token))
    bot.sendMessage(chat_id=chat_id, text=welcome_message)

    bot.sendMessage(chat_id=chat_id, text=first_message)

def on_text_message(bot, update):
    chat_id = update.message.chat_id
    if update.message.text == 'Прочитал, очень интересно!)':
        bot.sendMessage(chat_id=chat_id, text='А ты хорош:)')
        md.set_read(token, chat_id, clients[chat_id]['passed'])
        # print('<<<<<',new_delay)
        #print("<<<<<",clients)
        clients[chat_id]['red_message'] = True
        # clients[chat_id]['timer'] = new_delay
        #print(clients)


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
                # print(clients)
                if client['red_message']:
                    # message = 'lorem ipsum'
                    timer, message = md.get_info(token, chat_id)
                    # print('!!',timer, message)
                    key_board = ReplyKeyboardMarkup([['Прочитал, очень интересно!)']], one_time_keyboard=True)
                    updater.bot.sendMessage(chat_id=chat_id, text=message, reply_markup=key_board)

                    client['red_message'] = False
                    client['timer'] = timer
                    client['passed'] = 0
                else:
                    continue
            else:
                client['timer'] -= 3
                client['passed'] += 3
        yield from asyncio.sleep(3)


if __name__ == '__main__':
    #variables
    # print(1)
    clients = dict()
    #print('test')

    # database init
    md = Courses()


    #token parsing
    parser = argparse.ArgumentParser(description='Run flash-course telegram bot by your token')
    parser.add_argument('token', help='Just add token;)',
                        type=str)
    token = parser.parse_args().token

    #telegram updater
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    bt_name = updater.bot.getMe()

    md.set_bot_name(token, bt_name['username'], '{0} {1}'.format(bt_name['first_name'], bt_name['last_name']))

    #handlers
    start_handler = CommandHandler('start', on_start_command)
    mesg_handler = MessageHandler([Filters.text], on_text_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mesg_handler)

    threads_targets = [updater_wrapper, async_loop_wrapper]
    for target in threads_targets:
        threading.Thread(target=target).start()


    # Todo in Bot Constructor
    # md.init_bot(token)

