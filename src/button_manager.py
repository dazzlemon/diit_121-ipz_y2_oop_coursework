from button import LeafButton, Menu
from typing import List


class buttonManager:
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
            'Even Week Day', 'even_week_day', self.week_day_menu
        )

        # main_menu.week_menu init
        self.whole_week_button = LeafButton(
            'Whole Week(Odd & Even)', 'whole_week', self.week_menu
        )
        self.odd_week_button = LeafButton('', '', self.week_menu)# TODO
        self.even_week_button = LeafButton('', '', self.week_menu)# TODO

        # main_menu.group_menu init
        # TODO

        # main_menu.teacher_menu init
        # TODO

        # main.menu.student_menu init
        # TODO


    def print_main_menu(self, message):
        self.current_menu = self.main_menu.callback
        self.main_menu.operation(message, self.main_menu.callback)


    def button_handler(self, update, _context):
        query = update.callback_query
        query.answer()

        callback_str = query.data
        if callback_str == 'exit':
            query.delete_message()
        elif callback_str == 'back' and self.menu_history:
            prev_menu = self.menu_history.pop()
            self.main_menu.operation(query.message, prev_menu)
        else:
            self.menu_history.append(self.current_menu)
            self.current_menu = callback_str
            self.main_menu.operation(query.message, callback_str)