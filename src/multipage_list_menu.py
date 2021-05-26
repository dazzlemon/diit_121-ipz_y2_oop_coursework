"""
ListMenus
"""
from typing         import List, Tuple
from telegram       import InlineKeyboardButton
from multipage_menu import MultiPageMenu

class MultiPageListMenu(MultiPageMenu):
    """
    Forces user to fill in new data(choice from long lists)
    """
    def __init__(
        self,
        options: List[Tuple[str, str]], arg_name: str, callback: str,
        has_parent: bool,
        options_per_page: int=10
    ):
        MultiPageMenu.__init__(self, has_parent)
        self.options = options
        self.options_per_page = options_per_page
        self.arg_name = arg_name
        self.callback = callback

        self._current_page = 0


    def max_page(self) -> int:
        return len(self.options) / self.options_per_page


    def keyboard(self) -> List[List[InlineKeyboardButton]]:
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
        return keyboard
