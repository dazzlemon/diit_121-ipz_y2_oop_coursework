"""
TELEGRAM BOT
"""

import logging
from typing       import Callable, List
from dataclasses  import dataclass
from telegram.ext import (Updater,
                         CommandHandler,
                         MessageHandler,
                         Filters,
                         CallbackQueryHandler)
from user         import User

class Bot:
    """
    TELEGRAM BOT
    """
    def __init__(
        self,
        token: str,
        commands: List[Command],
        default_handler=None, button_handler=None
    ):
        self._updater = Updater(token=token, use_context=True)
        self._dispatcher = self._updater.dispatcher

        self._commands = commands
        self._init_commands()

        self._default_handler = default_handler
        self._init_default_handler()

        self._init_button_handler(button_handler)
        self._init_logging()


    def _init_default_handler(self):
        if self._default_handler is not None:
            handler = MessageHandler(
                Filters.text & (~Filters.command),
                self._default_handler
            )
            self._dispatcher.add_handler(handler)


    def _init_commands(self):
        for command in self._commands:
            handler = CommandHandler(command.keyword, command.handler)
            self._dispatcher.add_handler(handler)


    def _init_button_handler(self, button_handler):
        if not button_handler is None:
            handler = CallbackQueryHandler(button_handler)
            self._dispatcher.add_handler(handler)


    @staticmethod
    def _init_logging():
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
        )


    def run(self):
        """START UPDATING BOT"""
        self._updater.start_polling()


@dataclass
class Command:
    """TELEGRAM BOT COMMAND HANDLER"""
    keyword: str
    handler: Callable[[User], str]
    description: str
        