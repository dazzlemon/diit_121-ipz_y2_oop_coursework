"""
MAIN
"""

from bot import Bot, Command
from buttons import MenuManager
from button_manager import buttonManager

commands = []
#menu_manager = MenuManager()
button_mgr = buttonManager()

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

def menu_handler(update, _context):
    msg = update.message.reply_text('Please choose: ')
    button_mgr.print_main_menu(msg)


commands.append(Command(
    'menu',
    menu_handler,
    'prints menu'
))

def echo(update, context):
    """normal messages handler"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


if __name__ == '__main__':
    bot = Bot(
        '1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY',
        commands, echo, button_mgr.button_handler#menu_manager.button_handler
    )
    bot.run()
