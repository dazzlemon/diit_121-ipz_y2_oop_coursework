from button import LeafButton, Menu


class buttonManager:
    def __init__(self):
        self.last_menu = None
        self.current_menu = None

        self.main_menu = Menu('Menu', 'menu')

        # main_menu init
        self.day_menu = Menu('Day', 'day', self.main_menu)
        self.week_menu = Menu('Week', 'week', self.main_menu)
        self.group_menu = Menu('Group', 'group', self.main_menu)
        self.teacher_menu = Menu('Teacher', 'teacher', self.main_menu)
        self.student_menu = Menu('Student', 'student', self.main_menu)

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
        self.main_menu.operation(message)


    def button_handler(self, update, context):
        query = update.callback_query
        query.answer()

        callback_str = query.data
        if callback_str == 'exit':
            query.delete_message()
        if callback_str == 'back' and self.last_menu is not None:
            self.last_menu.operation(update, context)
