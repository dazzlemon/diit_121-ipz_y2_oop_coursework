"""
Additional class to choose suffix for callback(read class desc)
"""
from typing import   List, Tuple
from button import   Button
from telegram import Message, InlineKeyboardButton, InlineKeyboardMarkup

class MultiPageMenu(Button):
    """
    Helps to choose additional callback info, it will be added to prefix
    after ';', so both suffix and new options should not have that symbol
    in options first str is button text, seccond is suffix to add if it's chosen
    """
    def __init__(
        self,
        options: List[Tuple[str, str]], suffix: str,
        options_per_page: int=10, parent=None
    ):
        self.options = options
        self.options_per_page = options_per_page
        self.suffix = suffix

        self.current_page = 0


    def operation(self, message: Message, command: str):
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
        # add 'Back' button
        # add 'Exit' button
        # {
        #     command: ,
        #     group_id: ,
        #     week_day: ,
        #     calendar_day: ,
        #     teacher_id: ,
        #     student_id: ,
        # }
