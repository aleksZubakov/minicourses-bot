import re
from subprocess import Popen
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.emoji import Emoji

from model.Courses import Courses

def flash_course_run(token):
    bot = Popen(['python3.5', 'flash_course.py', token])

def on_start_command(bot, update):
    chat_id = update.message.chat_id
    clients[chat_id] = dict()
    clients[chat_id]['got_token'] = clients[chat_id]['add_message_flag'] \
        = clients[chat_id]['add_description_flag'] = clients[chat_id]['add_tag_flag'] \
        = clients[chat_id]['last_message_flag'] = False

    start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text='Привет! Вы попали в @sympolab_bot. Выбирайте действие:)',
                    reply_markup=start_keyboard)


def on_done_command(bot, update):
    chat_id = update.message.chat_id
    current_token = clients[chat_id]['current_token']

    # now client can't add new message
    clients[chat_id]['add_message_flag'] = False

    if not clients[chat_id][current_token]['messages']:
        add_message_keyboard = ReplyKeyboardMarkup(add_message_button + main_menu_button)
        bot.sendMessage(chat_id=chat_id, text='Извините, но бот не создан, поскольку вы не ввели ни одного сообщения',
                        reply_markup=add_message_keyboard)
        return

    raw_data = dict()

    author = update.message.from_user
    raw_data['author'] = "{0} {1}".format(author['first_name'], author['last_name'])

    info = clients[chat_id][current_token]
    raw_data['messages'] = info['messages']
    raw_data['tags'] = info['tags']
    raw_data['description'] = info['description']
    raw_data['timestamp'] = int(time.time())

    raw_data['token'] = current_token
    raw_data['last_message'] = info['last_message']
    md.init_bot(raw_data)

    flash_course_run(current_token)

    start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, resize_keyboard=False, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text='Поздравляем! Ваш бот успешно создан. Удачи!:)', reply_markup=start_keyboard)



def on_message_handler(bot, update):
    msg = update.message.text
    chat_id = update.message.chat_id

    if msg in helpers:
        helpers[msg](bot, chat_id)
        return

    if clients[chat_id]['got_token']:

        token = update.message.text
        valide_token = bool(re.match(r'[0-9]{9}:.+', token))

        #if valide create record for client
        if valide_token:
            if not chat_id in clients:
                clients[chat_id] = dict()

            clients[chat_id][token] = dict()
            clients[chat_id][token]['messages'] = list()
            clients[chat_id]['current_token'] = token

            bot.sendMessage(chat_id=chat_id, text='Отлично! Вы ввели правильный токен! Отправьте описание '
                                                  'вашего микрокурса в следующем сообщении')
            clients[chat_id]['add_description_flag'] = True

        else:
            start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, one_time_keyboard=True,
                                                 resize_keyboard=False)
            bot.sendMessage(chat_id=chat_id, text='Извините, но токен не валидный.', reply_markup=start_keyboard)

        clients[chat_id]['got_token'] = False
        return

    current_token = clients[chat_id]['current_token']
    msg = update.message.text # !

    if clients[chat_id]['add_description_flag']:
        clients[chat_id]['add_description_flag'] = False
        clients[chat_id]['add_tag_flag'] = True

        clients[chat_id][current_token]['description'] = msg

        bot.sendMessage(chat_id=chat_id, text='Превосходно! Напишите 1-3 тега к вашему курсу в '
                                              'следующем сообщении \n \nили введите /cancel')

        return

    if clients[chat_id]['add_tag_flag']:
        clients[chat_id]['add_tag_flag'] = False
        clients[chat_id]['last_message_flag'] = True

        clients[chat_id][current_token]['tags'] = msg.lower().split(' ')

        bot.sendMessage(chat_id=chat_id, text='Чудесно! Теперь напишите сообщение, которое будет заключительным'
                                              'для вашего курса(можно оставить ссылку на ваш основной проект).')

        return

    if clients[chat_id]['last_message_flag']:
        clients[chat_id]['last_message_flag'] = False
        clients[chat_id]['add_message_flag'] = True

        clients[chat_id][current_token]['last_message'] = msg

        bot.sendMessage(chat_id=chat_id, text='Прекрасно! Теперь добавляйте по одному сообщению к своему курсу. '
                                              'Когда закончите, напишите /done \n \nесли хотите прервать '
                                              'напишите /cancel')
        return

    if clients[chat_id]['add_message_flag']:
        # add message to bot token
        clients[chat_id][current_token]['messages'].append(update.message.text)

        return


""" Helpers"""


def helper_help(bot, chat_id):
    help_msg = 'Модуль в разработке.'
    help_cancel_keyboard = ReplyKeyboardMarkup(main_menu_button, one_time_keyboard=True, resize_keyboard=False)
    bot.sendMessage(chat_id=chat_id, text=help_msg, reply_markup=help_cancel_keyboard)


def helper_got_token(bot, chat_id):
    clients[chat_id]['got_token'] = True
    bot.sendMessage(chat_id=chat_id, text='Введите токен')


def helper_main_menu(bot, chat_id):
    clients[chat_id]['add_message_flag'] = clients[chat_id]['got_token'] = False
    start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, one_time_keyboard=True, resize_keyboard=False)
    bot.sendMessage(chat_id=chat_id, text='Отменено', reply_markup=start_keyboard)


def helper_create_new_course(bot, chat_id):
    create_msg = "{0} Откройте @BotFather.  Для этого нажмите его имя".format(emoji_nums[1]) + '\n' + \
                 "{0} С его помощью создай нового бота. Для этого нажмите 'new bot' внутри @BotFather".format(
                     emoji_nums[2]) + '\n' + \
                 "{0} Скопируйте API token, который он тебе даст.".format(emoji_nums[3]) + '\n' + \
                 "{0} Вернитесь обратно в @sypmolab_bot и отправьте сюда скопированный API токен".format(emoji_nums[4])
    got_token_keyboard = ReplyKeyboardMarkup(got_token_button + main_menu_button, one_time_keyboard=True,
                                             resize_keyboard=False)
    bot.sendMessage(chat_id=chat_id, text=create_msg, reply_markup=got_token_keyboard)


def helper_add_new_message(bot, chat_id):
    clients[chat_id]['add_message_flag'] = True
    bot.sendMessage(chat_id=chat_id, text='Напишите что хочешь добавить в свой микрокурс.')


if __name__ == '__main__':
    token = '294379760:AAG09m0GKPJfj1J0aNF0QUCd23WrLMUuz8M'
    clients = dict()
    md = Courses()

    # bot
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    emoji_nums = [Emoji.DIGIT_ZERO_PLUS_COMBINING_ENCLOSING_KEYCAP,
                  Emoji.DIGIT_ONE_PLUS_COMBINING_ENCLOSING_KEYCAP,
                  Emoji.DIGIT_TWO_PLUS_COMBINING_ENCLOSING_KEYCAP,
                  Emoji.DIGIT_THREE_PLUS_COMBINING_ENCLOSING_KEYCAP,
                  Emoji.DIGIT_FOUR_PLUS_COMBINING_ENCLOSING_KEYCAP]

    # buttons
    new_course_button = [[KeyboardButton(text='Создать новый микрокурс')]]
    help_button = [[KeyboardButton(text='Помощь')]]
    main_menu_button = [[KeyboardButton(text='Главное меню')]]
    add_message_button = [[KeyboardButton(text='Добавить сообщение в микрокурс')]]
    got_token_button = [[KeyboardButton(text='Я получил токен')]]
    add_description_button = [[KeyboardButton(text='Добавить описание')]]

    # helpers
    helpers = {'Создать новый микрокурс': helper_create_new_course,
               'Помощь': helper_help,
               'Главное меню': helper_main_menu,
               'Я получил токен': helper_got_token,
               'Добавить сообщение в микрокурс': helper_add_new_message}
               # 'Добавить описание' : helper_add_description}

    # handlers
    start_message = CommandHandler('start', on_start_command)
    on_message = MessageHandler([Filters.text], on_message_handler)
    on_done = CommandHandler('done', on_done_command)

    dispatcher.add_handler(start_message)
    dispatcher.add_handler(on_message)
    dispatcher.add_handler(on_done)

    updater.start_polling()
