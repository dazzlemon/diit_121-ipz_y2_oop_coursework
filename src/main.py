"""
TELEGRAM BOT
"""

import logging
from telegram.ext import Updater, CommandHandler

updater = Updater(
    token='1815999083:AAFClF7cEZq6IjXTxGNA07WQ5xLvZsKs6LY',
    use_context=True
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="VOT ETO DA"
    )

start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)

updater.start_polling()
