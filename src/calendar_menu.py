"""
Menu to choose calendar day
"""

import calendar
from datetime       import date
from typing         import List
from telegram       import InlineKeyboardButton
from multipage_menu import MultiPageMenu


class CalendarMenu(MultiPageMenu):
    """
    MENU TO CHOOSE CALENDAR DAY, callback is <CALENDAR_DAY=YYYY/MM/DD>
    """
    def __init__(self,
        start: date, finish: date, has_parent: bool, callback: str
    ):
        MultiPageMenu.__init__(self, has_parent)
        self.start = start
        self.finish = finish
        self.callback = callback

        self.current_page = 0


    def max_page(self) -> int:
        return ((self.finish.year - self.start.year) * 12
             + (self.finish.month - self.start.month))


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


    def _add_month_days(
        self, keyboard: List[List[InlineKeyboardButton]], year: int, month: int
    ):
        my_calendar = calendar.monthcalendar(year, month)
        for week in my_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(self.empty_button())
                else:
                    row.append(self._day_button(year, month, day))
            keyboard.append(row)


    def _day_button(self, year: int, month: int, day: int):
        """returns button for non 0 day"""
        return InlineKeyboardButton(
            day,
            callback_data='CALENDAR_DAY=%s/%s/%s' % (
                year, month, day
            ) + ';' + self.callback
        )
