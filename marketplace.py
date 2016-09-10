import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from model.Courses import Courses
import pymongo

# Setup database
client = pymongo.MongoClient()
db = client['courses']
# TODO here is test purposes
collection = db['test']

# setup updater, dispatcher, and logging
updater = Updater( token='216141785:AAHp0UsV5wnG03KuAMhbjxafw_9LujrdkSs' )
dispatcher = updater.dispatcher
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING )

# wrappers
def add_handlers( handlers ):
    for handler in handlers:
        dispatcher.add_handler( handler )



# unknown command handler
# def on_unknown_command(bot, update):
#     bot.sendMessage( chat_id=update.message.chat_id,
#                      text="Sorry, but I don't know what {0} means".format(update.message.text))
#
# on_unknown_handler = MessageHandler( [ Filters.command ], on_unknown_command )

def on_start_command( bot, update ):

    courses = collection.find().sort( 'connections_count', -1 )
    i = 1
    messages = list()
    for ent in courses:
        msg = u"""{0}: {1}
        {2}
        Link: {3}
        By {4}, \U0001F464 ({5})
        Tags: {6}""".format(i,
                   ent['screen_name'],
                   ent['description'],
                   '@'+ ent['bot_name'],
                   ent['author'],
                   ent['connections_count'],
                   ent['tags']
                   )
        messages.append( msg )
        i += 1

    bot.sendMessage( chat_id=update.message.chat_id,
                     text='\n'.join(messages))


# assign handlers
add_handlers( [ CommandHandler( 'start', on_start_command ) ] )



# start your engines
updater.start_polling()