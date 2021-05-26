"""
Menu to choose calendar day
"""

import calendar
from datetime       import date
from typing         import List
from telegram       import Message, InlineKeyboardMarkup, InlineKeyboardButton
from user           import User
from multipage_menu import MultiPageMenu


class CalendarMenu(MultiPageMenu):
    """
    MENU TO CHOOSE CALENDAR DAY, callback is <CALENDAR_DAY=YYYY/MM/DD>
    """
    def __init__(self,
        start: date, finish: date, has_parent: bool, callback: str
    ):
        self.start = start
        self.finish = finish
        self._has_parent = has_parent
        self.callback = callback

        self.current_page = 0


    @property
    def has_parent(self) -> bool:
        return self._has_parent


    def max_page(self) -> int:
        return ((self.finish.year - self.start.year) * 12
             + (self.finish.month - self.start.month))


    @property
    def current_page(self) -> int:
        return self._current_page


    @current_page.setter
    def current_page(self, val: int):
        self._current_page = val


    def keyboard(self) -> List[List[InlineKeyboardButton]]:
        keyboard: List[List[InlineKeyboardButton]] = []

        month = self.start.month + self.current_page - 1# 0 based
        year  = int(self.start.year + month / 12)
        month = month % 12
        month += 1# 1 based

        keyboard.append([InlineKeyboardButton(
            '%s %s' % (calendar.month_name[month], year), callback_data='pass'
        )])
        keyboard.append(self.weekdays_names())
        self._add_month_days(keyboard, year, month)
        return keyboard


    @staticmethod
    def weekdays_names():
        """
        returns row of buttons with weekday names with empty callbacks('pass')
        """
        row = []
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            row.append(InlineKeyboardButton(day, callback_data='pass'))
        return row


    def _add_month_days(self, keyboard, year, month):
        my_calendar = calendar.monthcalendar(year, month)
        for week in my_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(self.empty_button())
                else:
                    row.append(self._day_button(year, month, day))
            keyboard.append(row)


    def _day_button(self, year, month, day):
        """returns button for non 0 day"""
        return InlineKeyboardButton(
            day,
            callback_data='CALENDAR_DAY=%s/%s/%s' % (
                year, month, day
            ) + ';' + self.callback
        )
