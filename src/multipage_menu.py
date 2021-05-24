"""
Additional class to choose arguments for LeafButtons(update User state)
"""
from typing   import List, Tuple
from telegram import Message, InlineKeyboardButton, InlineKeyboardMarkup
from button   import Button, Menu
from user     import User


class MultiPageMenu(Button):
    """
    Forces user to fill in new data(choice from long lists)
    """
    def __init__(
        self,
        options: List[Tuple[str, str]], arg_name: str, callback: str,
        options_per_page: int=10, parent: Menu=None
    ):
        self.options = options
        self.options_per_page = options_per_page
        self.arg_name = arg_name
        self.callback = callback

        if parent is not None:
            parent.add(self)

        self.current_page = 0


    def callback_args(self) -> str:
        return ''


    def operation(self, message: Message, command: str, user_info: User):
        keyboard: List[List[InlineKeyboardButton]] = []
        for i in range(self.options_per_page):
            current_option_n = self.current_page * self.options_per_page + i

            # print(f'curr_option_n = {current_option_n}')# TODO: DEBUG
            # print(f'curr_page = {self.current_page}')# TODO: DEBUG
            # print(f'opt_per_page = {self.options_per_page}')# TODO: DEBUG
            # print(f'len opts = {len(self.options)}')# TODO: DEBUG

            if current_option_n >= len(self.options):
                break
            current_option = self.options[current_option_n]
            text = current_option[0]
            callback = f'{self.callback};{self.arg_name}={current_option[1]}'

            keyboard.append([InlineKeyboardButton(
                text,
                callback_data=callback
            )])
        print('test0')# printed# TODO: DEBUG
        if self.current_page > 0:
            pass# TODO: add '<'# prev page button
        if self.current_page < len(self.options) / self.options_per_page:
            pass# TODO: add '>'# next page button
        print('test01')#TODO: DEBUG#printed

        # if self.parent is not None:# TODO: doesnt work when this is uncommented
        #     keyboard.append([])
        #     keyboard[-1].append(
        #         InlineKeyboardButton('Back', callback_data='back')
        #     )
        print('test02')# TODO: DEBUG# not printed
        keyboard.append([])
        keyboard[-1].append(
            InlineKeyboardButton('Exit', callback_data='exit')
        )

        # for row in keyboard:
        #     for button in row:
        #         print(button)# TODO: DEBUG
        # print(f'keybord len = {len(keyboard)}')
        print('test')# not printed

        markup = InlineKeyboardMarkup(keyboard)
        message.edit_reply_markup(reply_markup=markup)