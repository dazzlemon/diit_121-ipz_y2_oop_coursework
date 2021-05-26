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
        options: List[Tuple[str, str]], arg_name: str, callback: str,
        has_parent: bool,
        options_per_page: int=10
    ):
        self.options = options
        self.options_per_page = options_per_page
        self.arg_name = arg_name
        self.callback = callback
        self.has_parent = has_parent

        self.current_page = 0


    def callback_args(self) -> str:
        return ''


    def operation(self, message: Message, command: str, user_info: User):
        keyboard: List[List[InlineKeyboardButton]] = []
        for i in range(self.options_per_page):
            current_option_n = self.current_page * self.options_per_page + i
            if current_option_n >= len(self.options):
                break
            current_option = self.options[current_option_n]
            text = current_option[0]
            callback = f'{self.callback};{self.arg_name}={current_option[1]}'

            keyboard.append([InlineKeyboardButton(
                text,
                callback_data=callback
            )])

        nav_buttons: List[InlineKeyboardButton] = []

        empty_button = InlineKeyboardButton(' ', callback_data='pass')

        if self.current_page > 0:
            nav_buttons.append(InlineKeyboardButton(
                '<',
                callback_data='prev_page'
            ))
        else:
            nav_buttons.append(empty_button)
        if self.current_page + 1 < len(self.options) / self.options_per_page:
            nav_buttons.append(InlineKeyboardButton(
                '>',
                callback_data='next_page'
            ))
        else:
            nav_buttons.append(empty_button)
        if self.options_per_page < len(self.options):
            keyboard.append(nav_buttons)

        if self.has_parent:
            keyboard.append([])
            keyboard[-1].append(
                InlineKeyboardButton('Back', callback_data='back')
            )
        keyboard.append([])
        keyboard[-1].append(
            InlineKeyboardButton('Exit', callback_data='exit')
        )

        markup = InlineKeyboardMarkup(keyboard)
        message.edit_reply_markup(reply_markup=markup)
