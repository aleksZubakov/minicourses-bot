import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from model.Courses import Courses
import pymongo

# Setup database
client = pymongo.MongoClient()
db = client['courses']
# TODO here is test purposes
collection = db['test']

# setup updater, dispatcher, and logging
updater = Updater( token='296973878:AAG8-Gu2ESh8rSbXX0S14R_8uJtC4opjCKY' )
dispatcher = updater.dispatcher
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING )

# wrappers
def add_handlers( handlers ):
    for handler in handlers:
        dispatcher.add_handler( handler )



# Globals
CURRENT_MODE = dict()
show_more = KeyboardButton('Показать еще')
popular = KeyboardButton('Популярное')
new = KeyboardButton('Новое')
tag_search = KeyboardButton('Поиск по тегам')

# unknown command handler
# def on_unknown_command(bot, update):
#     bot.sendMessage( chat_id=update.message.chat_id,
#                      text="Sorry, but I don't know what {0} means".format(update.message.text))
#
# on_unknown_handler = MessageHandler( [ Filters.command ], on_unknown_command )

def on_start_command( bot, update ):

    courses = collection.find().sort( 'connections_count', -1 )
    i = 0
    messages = list()
    messages.append('ПОПУЛЯРНОЕ /')
    data = list(courses)
    for ent in data:
        i += 1
        msg = u"""{0}: {1}
        {2}
        Link: {3}
        By {4}, \U0001F464 ({5})
        Tags: {6}
        TOK: {7}""".format(i,
                   ent['screen_name'],
                   ent['description'],
                   '@'+ ent['bot_name'],
                   ent['author'],
                   ent['connections_count'],
                   ent['tags'],
                   ent['token']
                   )
        messages.append( msg )
        if i == 3:
            break

    chat_id = str(update.message.chat_id)
    CURRENT_MODE[chat_id] = {
        'mode': 'mp',
        'from': i,
        'data': data[i:]
    }
    # print('!!!',CURRENT_MODE, CURRENT_MODE[chat_id], '\n', CURRENT_MODE[chat_id]['data'])

    repl = ReplyKeyboardMarkup([[show_more],
                                [new]])

    bot.sendMessage( chat_id=update.message.chat_id,
                     text='\n'.join(messages),
                     reply_markup=repl)


def on_message( bot, update ):
    chat_id = update.message.chat_id
    message = update.message.text
    if message == 'Показать еще':
        i = 0
        messages = []
        # print('>>', CURRENT_MODE)
        # print('>>',CURRENT_MODE[str(chat_id)])
        # print('>>', CURRENT_MODE[str(chat_id)]['data'])
        for ent in CURRENT_MODE[str(chat_id)]['data']:
            i += 1
            msg = u"""{0}: {1}
             {2}
             Link: {3}
             By {4}, \U0001F464 ({5})
             Tags: {6}
             TOK: {7}""".format(i + CURRENT_MODE[str(chat_id)]['from'],
                                ent['screen_name'],
                                ent['description'],
                                '@' + ent['bot_name'],
                                ent['author'],
                                ent['connections_count'],
                                ent['tags'],
                                ent['token']
                                )
            messages.append(msg)
            if i == 3:
                break

        if i < 3:
            extra_msg = "\nБольше нету :(, создай свой крутой курс на @SYMPO_CREATE"
        else:
            extra_msg = ''
        messages.append(extra_msg)
        if CURRENT_MODE[chat_id]['mode'] == 'mp':
            but1 = new
            but2 = tag_search
        elif CURRENT_MODE[chat_id]['mode'] == 'new':
            but1 = popular
            but2 = tag_search
        elif CURRENT_MODE[chat_id]['mode'] == 'tg':
            but1 = popular
            but2 = new
        else:
            but1  = new
            but2 = popular

        repl = ReplyKeyboardMarkup([[but1],[but2]])
        bot.sendMessage(chat_id, "\n".join(messages), repl)
    elif message == 'Популярное':
        courses = collection.find().sort('connections_count', -1)
        i = 0
        messages = list()
        data = list(courses)
        for ent in data:
            i += 1
            msg = u"""{0}: {1}
                {2}
                Link: {3}
                By {4}, \U0001F464 ({5})
                Tags: {6}
                TOK: {7}""".format(i,
                                   ent['screen_name'],
                                   ent['description'],
                                   '@' + ent['bot_name'],
                                   ent['author'],
                                   ent['connections_count'],
                                   ent['tags'],
                                   ent['token']
                                   )
            messages.append(msg)
            if i == 3:
                break

        chat_id = str(update.message.chat_id)
        CURRENT_MODE[chat_id] = {
            'mode': 'mp',
            'from': i,
            'data': data[i:]
        }

        repl = ReplyKeyboardMarkup([[new], [tag_search]])

        bot.sendMessage( chat_id=update.message.chat_id,
                         text='\n'.join(messages)
                         )




# assign handlers
add_handlers( [ CommandHandler( 'start', on_start_command ) , MessageHandler([Filters.text], on_message)])



# start your engines
updater.start_polling()