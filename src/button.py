"""
Button hierarchy for telegram bot menu
"""

from __future__ import annotations
from abc        import ABC, abstractmethod
from typing     import List, Callable
from telegram   import InlineKeyboardMarkup, InlineKeyboardButton, Message


class Button(ABC):
    """
    Component from Composite Pattern,
    either prints result of its handler or prints new menu when clicked
    (unless its 'Exit' or 'Back', these just exit the menu or go to the previous
    respectively)
    """
    @property
    def parent(self) -> Menu:
        """
        parent of this Button, needed to check if 'Back' button is needed
        """
        return self._parent


    @parent.setter
    def parent(self, parent: Button):
        self._parent = parent


    @abstractmethod
    def operation(
        self, message: Message, command: str, arg1: str=None, arg2: str=None
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
        handler: Callable[[], str]=None,
        arg1_name: str=None, arg2_name: str=None
    ):
        """added to parent automatically"""
        self.text = text
        self.callback = callback
        self.handler = handler

        self.arg1_name = arg1_name
        self.arg2_name = arg2_name

        if parent is not None:
            parent.add(self)


    def operation(
        self, message: Message, command: str, arg1: str=None, arg2: str=None
    ) -> bool:
        """
        call for the handler
        """
        if command == self.callback:
            new_text = f'leaf button: {self.text}'
            if self.handler is not None:
                if arg1 is None and self.arg1_name is not None:
                    pass# TODO: get arg1
                elif arg2 is None and self.arg2_name is not None:
                    pass# TODO: get arg2
                else:# both args aren't None or it's okay if one of them is
                    new_text = self.handler(arg1, arg2)

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
        parent: Menu=None
    ) -> None:
        self._children: List[List[Button]] = [[]]
        self.parent = parent
        self.text = text
        self.callback = callback

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
        self, message: Message, command: str, arg1: str=None, arg2: str=None
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
                        button.text, callback_data=button.callback
                    ),
                    row
                )),
                self._children
            ))

            if self.parent is not None:
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
                    result = button.operation(message, command, arg1, arg2)
                    if result:
                        return True
