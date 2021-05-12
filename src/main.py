"""
MAIN
"""

from bot import Bot, Command
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

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

def menu(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Whole schedule', callback_data='Whole schedule'),
            InlineKeyboardButton('Schedule for this week', callback_data='Schedule for this week'),
        ],
        [
            InlineKeyboardButton('Schedule for today', callback_data='Schedule for today'),
            InlineKeyboardButton('Schedule for tomorrow', callback_data='Schedule for tomorrow'),
        ],
        [
            InlineKeyboardButton('Current subject', callback_data='Current subject'),
            InlineKeyboardButton('Next subject', callback_data='Next subject'),
        ],
        [
            InlineKeyboardButton('more', callback_data='more'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
commands.append(Command(
    'menu',
    menu,
    'prints menu'
))

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

def echo(update, context):
    """normal messages handler"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )

bot = Bot('1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY', commands, echo, button)

if __name__ == '__main__':
    bot.run()
