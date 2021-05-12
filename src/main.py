"""
MAIN
"""

from bot import Bot, Command
from buttons import menu, button

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

commands.append(Command(
    'menu',
    menu,
    'prints menu'
))

def echo(update, context):
    """normal messages handler"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )

bot = Bot('1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY', commands, echo, button)

if __name__ == '__main__':
    bot.run()
