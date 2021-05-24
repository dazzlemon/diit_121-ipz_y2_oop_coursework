"""
Button manager for timetable bot, using button module
"""

from button import LeafButton, Menu


class ButtonManager:
    """
    Button manager for timetable bot, using button module
    """
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
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
        self.sql_conn.execute("""REPLACE INTO USER
                (CURRENT_MENU, MENU_HISTORY, ID)
            VALUES
                ('%s', '', %s)""" % (self.main_menu.callback, message.chat_id)
        )
        self.sql_conn.commit()
        self.main_menu.operation(message, self.main_menu.callback)


    def button_handler(self, update, _context):
        """
        handles callback buttons
        """
        # callback data is limited with 64bytes, so it will contain command
        # + two arguments in special order, delimited by ';'
        # in case of this specific application no commands need more than two
        # args at the same time(most need just the group_id)
        # so this is sufficient, but in other cases another database
        # for each chat and its arguments would probably be needed,
        # or some weird compression
        query = update.callback_query
        query.answer()

        callback_tuple = query.data.split(';')

        while len(callback_tuple) < 3:
            callback_tuple += (None,)# append None args to unpack
        callback_str, arg1, arg2 = callback_tuple

        row = next(self.sql_conn.execute("""SELECT MENU_HISTORY, CURRENT_MENU
            FROM USER
            WHERE ID = %s""" % update.effective_chat.id))

        menu_history_str = row[0]
        current_menu = row[1]

        menu_history = menu_history_str.split(';')

        if callback_str == 'exit':
            query.delete_message()
        elif callback_str == 'back' and menu_history:
            current_menu = menu_history.pop()
            self.main_menu.operation(
                query.message, current_menu, arg1, arg2
            )
        else:
            if self.main_menu.operation(
                query.message, callback_str, arg1, arg2
            ):
                menu_history.append(current_menu)
                current_menu = callback_str

        menu_history_str = ';'.join(menu_history)
        self.sql_conn.execute("""REPLACE INTO USER
                (CURRENT_MENU, MENU_HISTORY, ID)
            VALUES
                ('%s', '%s', %s)""" % (
                    current_menu, menu_history_str, update.effective_chat.id
                )
        )
        self.sql_conn.commit()
