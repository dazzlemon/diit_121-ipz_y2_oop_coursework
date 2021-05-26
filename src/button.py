"""
Button hierarchy for telegram bot menu
"""

from __future__ import annotations
from abc        import ABC, abstractmethod
from typing     import List, Callable
from telegram   import InlineKeyboardMarkup, InlineKeyboardButton, Message
from user       import User


class Button(ABC):
    """
    Component from Composite Pattern,
    either prints result of its handler or prints new menu when clicked
    (unless its 'Exit' or 'Back', these just exit the menu or go to the previous
    respectively)
    """


    def callback_args(self) -> str:
        """returns additional data to be added to callback"""
        return ''


    @abstractmethod
    def operation(
        self, message: Message, command: str, user_info: User
    ) -> bool:
        """
        Changes parameter message, performed if command == callback
        True -> changed menu
        Fales -> didnt change menu
        None -> Bad command(Nothing happend)
        """


class LeafButton(Button):
    """
    Leaf from Composite Pattern
    Doesnt print new menu when clicked,
    just calls handler and prints the result
    arg2 is not None only if arg1 is not None
    """
    def __init__(
        self,
        text: str, callback: str, parent: Menu,
        handler: Callable[[User], str]=None,
        arg1name: str=None, arg2name: str=None
    ):
        """added to parent automatically"""
        self.text     = text
        self.callback = callback
        self.handler  = handler
        self.arg1name = arg1name
        self.arg2name = arg2name
        if parent is not None:
            parent.add(self)


    def callback_args(self) -> str:
        cb_args = ''
        if self.arg1name is not None:
            cb_args += ';!' + self.arg1name
        if self.arg2name is not None:
            cb_args += ';!' + self.arg2name
        return cb_args


    def operation(
        self, message: Message, command: str, user_info: User
    ) -> bool:
        """
        call for the handler
        """
        if command == self.callback:
            new_text = f'leaf button: {self.text}'
            if self.handler is not None:
                new_text = self.handler(user_info)
            message.edit_text(new_text)
            message.edit_reply_markup(reply_markup=None)
            # raises BadRequest, but everything works as intended

            return False


class Menu(Button):
    """
    Composite from the pattern of the same name
    Prints menu with all the children when clicked, also prints 'Exit' option,
    and 'Back' if has parent, if 'Back' is clicked than parent is called(printed)
    """

    def __init__(
        self,
        text: str, callback: str,
        parent: Menu=None,
    ) -> None:
        self._children: List[List[Button]] = [[]]
        self.has_parent = parent is not None
        self.text       = text
        self.callback   = callback
        if parent is not None:
            parent.add(self)


    def add(self, button: Button) -> None:
        """adds button to the current row"""
        self._children[-1].append(button)


    def remove(self, button: Button) -> None:
        """removes button if its in the keyboard"""
        for row in self._children:
            row.remove(button)


    def next_row(self):
        """go to the next row(if current row is empty does nothing)"""
        if self._children[-1]:
            self._children.append([])


    def operation(
        self, message: Message, command: str, user_info: User
    ) -> bool:
        """
        Print all Children in the order they were added, first row wise,
        then in row
        + 'Back if has parent', callback = 'back'
        + 'Exit', callback = 'exit'
        """
        if command == self.callback:
            keyboard = list(map(
                lambda row: list(map(
                    lambda button: InlineKeyboardButton(
                        button.text, callback_data=(button.callback +
                        button.callback_args())
                    ),
                    row
                )),
                self._children
            ))

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
            return True
        else:
            for row in self._children:
                for button in row:
                    if button.operation(message, command, user_info):
                        return True
