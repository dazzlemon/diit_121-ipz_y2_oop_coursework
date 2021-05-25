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

    
    def operation(self, message: Message, command: str, user_info: User):
        keyboard: List[List[InlineKeyboardButton]] = []

        month = self.start.month + self.current_page - 1# 0 based
        year  = int(self.start.year + month / 12)
        month = month % 12
        month += 1# 1 based

        #First row - Month and Year
        row = []
        row.append(
            InlineKeyboardButton(
                '%s %s' % (calendar.month_name[month], year),
                callback_data='pass'
            )
        )
        keyboard.append(row)
        #Second row - Week Days
        row = []
        for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
            row.append(InlineKeyboardButton(day, callback_data='pass'))
        keyboard.append(row)

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
        #Last row - Buttons
        nav_buttons: List[InlineKeyboardButton] = []

        empty_button = InlineKeyboardButton(' ', callback_data='pass')

        if self.current_page > 0:
            nav_buttons.append(InlineKeyboardButton(
                '<',
                callback_data='prev_page'
            ))
        else:
            nav_buttons.append(empty_button)
        diff = ((self.finish.year - self.start.year) * 12
             + (self.finish.month - self.start.month))
        if self.current_page + 1 < diff:
            nav_buttons.append(InlineKeyboardButton(
                '>',
                callback_data='next_page'
            ))
        else:
            nav_buttons.append(empty_button)
        if nav_buttons != []:
            keyboard.append(nav_buttons)

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
