"""
Button hierarchy for telegram bot menu
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Button(ABC):
    """
    Component from Composite Pattern
    """
    @property
    def parent(self) -> Button:
        return self._parent


    @parent.setter
    def parent(self, parent: Button):
        self._parent = parent


    def add(self, button: Button) -> None:
        pass


    def remove(self, button: Button) -> None:
        pass


    def is_composite(self) -> bool:
        return False


    @abstractmethod
    def operation(self) -> str:
        pass


class LeafButton(Button):
    """
    Leaf from Composite Pattern
    Doesnt print new menu when clicked,
    just calls handler and prints the result
    """
    def operation(self) -> str:
        """
        call for the handler
        """


class Menu(Button):
    """
    Composite from the pattern of the same name
    Prints menu with all the children when clicked, also prints 'Exit' option,
    and 'Back' if has parent, if 'Back' is clicked than parent is called(printed)
    """

    def __init__(self) -> None:
        self._children: List[Button] = []


    def add(self, button: Button) -> None:
        self._children.append(button)
        button.parent = self


    def remove(self, component: Button) -> None:
        self._children.remove(component)
        component.parent = None


    def is_composite(self) -> bool:
        return True


    def operation(self) -> str:
        """
        Print all Children
        """
