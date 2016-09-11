from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.emoji import Emoji


def on_start_command(bot, update):
    chat_id = update.message.chat_id
    clients[chat_id] = dict()
    clients[chat_id]['got_token'] = clients[chat_id]['add_flag'] = False

    start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text='Привет! Ты попал в @sympocreator_bot. Выбирай действие:)', reply_markup=start_keyboard)

def on_done_command(bot, update):
    pass

def on_message_handler(bot, update):
    msg = update.message.text
    chat_id = update.message.chat_id

    if msg in helpers:
        helpers[msg](bot, chat_id)
        return

    if clients[chat_id]['add_flag']:
        # get current bot token
        current_token = clients[chat_id]['current_token']
        # add message to bot token
        clients[chat_id][current_token].append(update.message.text)

        # now client can't add new message
        clients[chat_id]['add_flag'] = False

        add_more_keyboard = ReplyKeyboardMarkup(add_more_button + main_menu_button, one_time_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text='Спасибо. Нажми кнопку добавить еще, если есть что добавить '
                                              'или выйди в главное меню.', reply_markup=add_more_keyboard)
        return

    if clients[chat_id]['got_token']:
        #todo write function to validate token!
        token = update.message.text
        valide_token = True

        #if valide create record for client
        if valide_token:
            if not chat_id in clients:
                clients[chat_id] = dict()

            #list of messages
            clients[chat_id][token] = list()
            clients[chat_id]['current_token'] = token

            add_message_button = [[KeyboardButton(text='Добавить сообщение в микрокурс')]]
            add_message_keyboard = ReplyKeyboardMarkup(add_message_button + main_menu_button,
                                                       one_time_keyboard=True)
            bot.sendMessage(chat_id=chat_id, text='Отлично! Вы ввели правильный токен!',
                            reply_markup=add_message_keyboard)

        else:
            start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button)
            bot.sendMessage(chat_id=chat_id, text='Извините, но токен не валидный.', reply_markup=start_keyboard)

        clients[chat_id]['got_token'] = False

""" Helpers"""
def helper_help(bot, chat_id):
    help_msg = 'Модуль в разработке.'
    help_cancel_keyboard = ReplyKeyboardMarkup(main_menu_button, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text=help_msg, reply_markup=help_cancel_keyboard)

def helper_got_token(bot, chat_id):
    clients[chat_id]['got_token'] = True
    bot.sendMessage(chat_id=chat_id, text='Введите токен')

def helper_main_menu(bot, chat_id):
    clients[chat_id]['add_flag'] = clients[chat_id]['got_token'] = False
    start_keyboard = ReplyKeyboardMarkup(new_course_button + help_button, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text='Отменено', reply_markup=start_keyboard)

def helper_create_new_course(bot, chat_id):
    create_msg = "{0} Открывай @BotFather. Жмякай для этого на его имя".format(emoji_nums[1]) + '\n' + \
                 "{0} С его помощью создай нового бота. Для этого нажми 'new bot' внутри @BotFather".format(
                     emoji_nums[2]) + '\n' + \
                 "{0} Скопируй API token, который он тебе даст.".format(emoji_nums[3]) + '\n' + \
                 "{0} Вернись обратно в @sypmocreator_bot и отправь сюда скопированный API token".format(emoji_nums[4])
    got_token_keyboard = ReplyKeyboardMarkup(got_token_button + main_menu_button, one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id, text=create_msg, reply_markup=got_token_keyboard)

def helper_add_new_message(bot, chat_id):
    clients[chat_id]['add_flag'] = True
    bot.sendMessage(chat_id=chat_id, text='Напиши что хочешь добавить в свой микрокурс.')


if __name__ == '__main__':
    token = '254385124:AAFzW49rQixpdUMfGpG3h2FYB049lDtBYJk'
    clients = dict()

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
    add_button = [[KeyboardButton(text='Добавить сообщение в микрокурс')]]
    add_more_button = [[KeyboardButton(text='Добавить еще')]]
    got_token_button = [[KeyboardButton(text='Я получил токен')]]

    # helpers
    helpers = {'Создать новый микрокурс': helper_create_new_course,
               'Помощь': helper_help,
               'Главное меню': helper_main_menu,
               'Я получил токен': helper_got_token,
               'Добавить сообщение в микрокурс': helper_add_new_message,
               'Добавить еще': helper_add_new_message}

    #handlers
    start_message = CommandHandler('start', on_start_command)
    on_message = MessageHandler([Filters.text], on_message_handler)
    on_done = CommandHandler('done', on_done_command)

    dispatcher.add_handler(start_message)
    dispatcher.add_handler(on_message)
    dispatcher.add_handler(on_done_command)

    updater.start_polling()