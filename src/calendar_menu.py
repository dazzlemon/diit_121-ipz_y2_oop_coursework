"""
Menu to choose calendar day
"""

import calendar
from datetime import date
from typing   import List
from telegram import Message, InlineKeyboardMarkup, InlineKeyboardButton
from button   import Button
from user     import User


class CalendarMenu(Button):
    """
    MENU TO CHOOSE CALENDAR DAY, callback is <CALENDAR_DAY=YYYY/MM/DD>
    """
    def __init__(self,
        start: date, finish: date, has_parent: bool, callback: str
    ):
        self.start = start
        self.finish = finish
        self.has_parent = has_parent
        self.callback = callback

        self.current_page = 0


    def callback_args(self) -> str:
        return ''


    def operation(self, message: Message, command: str, user: User):
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
        self._add_page_nav_buttons(keyboard)
        self._add_nav_buttons(keyboard)

        markup = InlineKeyboardMarkup(keyboard)
        message.edit_reply_markup(reply_markup=markup)


    @staticmethod
    def weekdays_names():
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
                    row.append(InlineKeyboardButton(" ", callback_data='pass'))
                else:
                    row.append(InlineKeyboardButton(
                        day,
                        callback_data='CALENDAR_DAY=%s/%s/%s' % (
                            year, month, day
                        ) + ';' + self.callback
                    ))
            keyboard.append(row)


    def _add_nav_buttons(self, keyboard):
        if self.has_parent:
            keyboard.append(
                [InlineKeyboardButton('Back', callback_data='back')]
            )
        keyboard.append(
            [InlineKeyboardButton('Exit', callback_data='exit')]
        )


    def _add_page_nav_buttons(self, keyboard):
        keyboard.append([self._prev_button(), self._next_button()])


    def _next_button(self):
        diff = ((self.finish.year - self.start.year) * 12
             + (self.finish.month - self.start.month))
        if self.current_page + 1 < diff:
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
        return InlineKeyboardButton(' ', callback_data='pass')
