"""
TELEGRAM BOT
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(
    token='1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY',
    use_context=True
)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

class Command:
    def __init__(self, keyword, handler, description):
        self.keyword = keyword
        self.handler = handler
        self.description = description

commands = []

def start(update, context):
    """/start handler"""
    descriptions = ''
    for command in commands:
        descriptions += '/' + command.keyword + ' - ' + command.description + '\n'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=descriptions
    )
commands.append(Command(
    'start',
    start,
    'info about commands'
))

def caps(update, context):
    """/caps handler"""
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )
commands.append(Command(
    'caps',
    caps,
    'repeats your message but capsed'
))

for command in commands:
    handler = CommandHandler(command.keyword, command.handler)
    dispatcher.add_handler(handler)

def echo(update, context):
    """normal messages handler"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
