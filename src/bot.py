"""
TELEGRAM BOT
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class Bot:
    """
    TELEGRAM BOT
    """
    def __init__(self, token, commands, default_handler=None):
        self._updater = Updater(
            token=token,
            use_context=True
        )
        self._dispatcher = self._updater.dispatcher
        self._commands = commands

        for command in commands:
            handler = CommandHandler(command.keyword, command.handler)
            self._dispatcher.add_handler(handler)

        self._default_handler = default_handler
        if not default_handler is None:
            handler = MessageHandler(
                Filters.text & (~Filters.command),
                default_handler
            )
            self._dispatcher.add_handler(handler)

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
        )

    def run(self):
        """START UPDATING BOT"""
        self._updater.start_polling()

class Command:
    """TELEGRAM BOT COMMAND HANDLER"""
    def __init__(self, keyword, handler, description):
        self.keyword = keyword
        self.handler = handler
        self.description = description
        