"""
Button hierarchy for telegram bot menu
"""

from __future__ import annotations
from abc        import ABC, abstractmethod
from typing     import List
from telegram   import InlineKeyboardMarkup, InlineKeyboardButton


class Button(ABC):
    """
    Component from Composite Pattern,
    either prints result of its handler or prints new menu when clicked
    (unless its 'Exit' or 'Back', these just exit the menu or go to the previous
    respectively)
    """
    @property
    def parent(self) -> Button:
        return self._parent


    @parent.setter
    def parent(self, parent: Button):
        self._parent = parent


    def is_composite(self) -> bool:
        return False


    @abstractmethod
    def operation(self, message, command) -> None:
        """
        Changes parameter message, performed if command == callback
        """


class LeafButton(Button):
    """
    Leaf from Composite Pattern
    Doesnt print new menu when clicked,
    just calls handler and prints the result
    """
    def __init__(self, text: str, callback: str, parent: Menu):
        """added to parent automatically"""
        self.text = text
        self.callback = callback

        if parent is not None:
            parent.add(self)


    def operation(self, message, command) -> None:
        """
        call for the handler
        """


class Menu(Button):
    """
    Composite from the pattern of the same name
    Prints menu with all the children when clicked, also prints 'Exit' option,
    and 'Back' if has parent, if 'Back' is clicked than parent is called(printed)
    """

    def __init__(self, text: str, callback: str, parent: Menu=None) -> None:
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


    def is_composite(self) -> bool:
        return True


    def operation(self, message, command) -> None:
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
        else:
            for row in self._children:
                for button in row:
                    button.operation(message, command)
