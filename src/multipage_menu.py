"""
Additional class to choose arguments for LeafButtons(update User state)
"""
from typing   import List
from abc      import abstractmethod
from telegram import Message, InlineKeyboardButton
from button   import Menu
from user     import User

class MultiPageMenu(Menu):
    """Multi page menu with scrolling"""
    def __init__(self, has_parent):
        Menu.__init__(self, has_parent)


    @property
    def has_parent(self) -> bool:
        """Needed to check if 'Back' button is needed"""
        return self._has_parent


    @property
    def current_page(self) -> int:
        """current page"""
        return self._current_page


    @current_page.setter
    def current_page(self, val: int):
        self._current_page = val


    @abstractmethod
    def max_page(self) -> int:
        """maxpage"""


    @abstractmethod
    def keyboard(self) -> List[List[InlineKeyboardButton]]:
        """keyboard base"""


    def operation(self, message: Message, command: str, user: User):
        self.print(message)


    def _additional_buttons(self, keyboard: List[List[InlineKeyboardButton]]):
        self._add_page_nav_buttons(keyboard)
        self._add_nav_buttons(keyboard)


    def _add_nav_buttons(self, keyboard: List[List[InlineKeyboardButton]]):
        if self.has_parent:
            keyboard.append(
                [InlineKeyboardButton('Back', callback_data='back')]
            )
        keyboard.append(
            [InlineKeyboardButton('Exit', callback_data='exit')]
        )


    def _add_page_nav_buttons(self, keyboard: List[List[InlineKeyboardButton]]):
        keyboard.append([self._prev_button(), self._next_button()])


    def _next_button(self):
        if self.current_page + 1 < self.max_page():
            return InlineKeyboardButton(
                '>',
                callback_data='next_page'
            )
        else:
            return self.empty_button()


    def _prev_button(self):
        if self.current_page > 0:
            return InlineKeyboardButton(
                '<',
                callback_data='prev_page'
            )
        else:
            return self.empty_button()


    @staticmethod
    def empty_button():
        """returns button with no text and 'pass' callback"""
        return InlineKeyboardButton(' ', callback_data='pass')
