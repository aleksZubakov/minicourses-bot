"""
Flash course comamnds handlers

"""

from telegram.ext import MessageHandler, Filters


def on_start_message(bot, update):
    chat_id = update.message.chat_id
    # db.set_new_client()
