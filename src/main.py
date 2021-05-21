"""
MAIN
"""

from bot import Bot, Command
from button_manager import buttonManager

commands = []
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


def menu_handler(update, _context):
    msg = update.message.reply_text('Please choose: ')
    button_mgr.print_main_menu(msg)
commands.append(Command(
    'menu',
    menu_handler,
    'prints menu'
))


if __name__ == '__main__':
    bot = Bot(
        '1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY',
        commands, None, button_mgr.button_handler#menu_manager.button_handler
    )
    bot.run()
