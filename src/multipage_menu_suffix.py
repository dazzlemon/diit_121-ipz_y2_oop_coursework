"""
Additional class to choose arguments for LeafButtons(update User state)
"""
from typing   import List, Tuple
from telegram import Message, InlineKeyboardButton, InlineKeyboardMarkup
from button   import Button
from user     import User


class MultiPageMenu(Button):
    """
    Forces user to fill in new data(choice from long lists)
    """
    def __init__(
        self,
        options: List[Tuple[str, str]], arg_name: str,
        options_per_page: int=10, parent=None
    ):
        self.options = options
        self.options_per_page = options_per_page
        self.arg_name = arg_name

        self.current_page = 0


    def operation(self, message: Message, command: str, user_info: User):
        keyboard: List[List[InlineKeyboardButton]] = []
        for i in range(self.options_per_page):
            current_option_n = self.current_page * self.options_per_page + i
            if current_option_n >= len(self.options):
                break
            current_option = self.options[current_option_n]
            text = current_option[0]
            callback = current_option[1]

            keyboard.append([InlineKeyboardButton(
                text,
                callback_data=callback
            )])
        if self.current_page > 0:
            pass# TODO: add '<'# prev page button
        if self.current_page < len(self.options) / self.options_per_page:
            pass# TODO: add '>'# next page button
        # TODO: add 'Back' button
        # TODO: add 'Exit' button

        markup = InlineKeyboardMarkup(keyboard)
        message.edit_reply_markup(reply_markup=markup)
