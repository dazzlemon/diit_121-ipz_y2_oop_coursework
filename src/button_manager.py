"""
Button manager for timetable bot, using button module
"""

from typing import List
from button import LeafButton, Menu


class ButtonManager:
    """
    Button manager for timetable bot, using button module
    """
    def __init__(self):
        self.menu_history: List[str] = []
        self.current_menu = None

        self.main_menu = Menu('Menu', 'menu')

        # main_menu init
        self.day_menu = Menu('Day', 'day', self.main_menu)
        self.main_menu.next_row()
        self.week_menu = Menu('Week', 'week', self.main_menu)
        self.main_menu.next_row()
        self.group_menu = Menu('Group', 'group', self.main_menu)
        self.main_menu.next_row()
        self.teacher_menu = Menu('Teacher', 'teacher', self.main_menu)
        self.main_menu.next_row()
        self.student_menu = Menu('Student', 'student', self.main_menu)
        self.main_menu.next_row()

        # main_menu.day_menu init
        self.today_button = LeafButton('Today', 'today', self.day_menu)
        self.tomorrow_button = LeafButton('Tomorrow', 'tomorrow', self.day_menu)
        self.calendar_day_button = LeafButton(
            'Calendar Day', 'calendar_day', self.day_menu
        )
        self.week_day_menu = Menu('Week Day', 'week_day', self.day_menu)

        # main_menu.day_menu.week_day_menu init
        self.wholeweek_day_button = LeafButton(
            'Whole Week(Odd & Even) Day', 'whole_week_day', self.week_day_menu
        )
        self.oddweek_day_button = LeafButton(
            'Odd Week Day', 'odd_week_day', self.week_day_menu
        )
        self.evenweek_day_button = LeafButton(
            'Even Week Day', 'even_week_day', self.week_day_menu, lambda: 'test'
        )

        # main_menu.week_menu init
        self.whole_week_button = LeafButton(
            'Whole Week(Odd & Even)', 'whole_week', self.week_menu
        )
        self.odd_week_button = LeafButton(
            'Odd Week', 'odd_week', self.week_menu
        )
        self.even_week_button = LeafButton(
            'Even Week', 'even_week', self.week_menu
        )

        # main_menu.group_menu init
        self.all_students_button = LeafButton(
            'All Students', 'all_students', self.group_menu
        )
        self.subgroup1_button = LeafButton(
            'Subgroup1', 'subgroup1', self.group_menu
        )
        self.subgroup2_button = LeafButton(
            'Subgroup2', 'subgroup2', self.group_menu
        )

        # main_menu.teacher_menu init
        self.teacher_info_button = LeafButton(
            'Info about teacher', 'teacher_info', self.teacher_menu
        )

        # main.menu.student_menu init
        self.student_info_button = LeafButton(
            'Info about student', 'student_info', self.student_menu
        )


    def print_main_menu(self, message):
        """
        creates new message with main menu keyboard
        """
        self.current_menu = self.main_menu.callback
        self.main_menu.operation(message, self.main_menu.callback)


    def button_handler(self, update, _context):
        """
        handles callback buttons
        """
        query = update.callback_query
        query.answer()

        callback_str = query.data
        if callback_str == 'exit':
            query.delete_message()
        elif callback_str == 'back' and self.menu_history:
            self.current_menu = self.menu_history.pop()
            self.main_menu.operation(query.message, self.current_menu)
        else:
            if self.main_menu.operation(query.message, callback_str):
                self.menu_history.append(self.current_menu)
                self.current_menu = callback_str
