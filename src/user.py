"""
user dataclass
"""

import datetime
from dataclasses import dataclass

@dataclass
class User:
    """
    Easier access to user specific data(args for commands)
    """
    group_id: int
    teacher_id: int
    calendar_day: str
    week_day: int
    class_id: int


    def weekday_from_calendar_day(self):
        """1 based day from calendar day"""
        return self.date_from_calendar_day().weekday() + 1


    def is_odd_week_from_calendar_day(self):
        """is week odd(year wise) from calendar day"""
        return self.date_from_calendar_day().isocalendar().week % 2 == 1


    def date_from_calendar_day(self):
        """datetime.date object from calendar_day"""
        year, month, day = self.calendar_day.split('/')
        return datetime.date(int(year), int(month), int(day))
