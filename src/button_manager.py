"""
Button manager for timetable bot, using button module
"""

import datetime
from typing          import List
from telegram        import CallbackQuery, Update
from button          import LeafButton, Menu
from user            import User
from multipage_menu  import MultiPageMenu
from sql             import Schedule
from calendar_menu   import CalendarMenu
from user_db_manager import UserDbManager


class ButtonManager:
    """
    Button manager for timetable bot, using button module
    """
    def __init__(self, user_db, schedule_db):
        self.user_db = UserDbManager(user_db)
        self.schedule_db = schedule_db
        self.main_menu = Menu('Menu', 'menu')

        self.current_updater = None
        self.schedule = Schedule(schedule_db)

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

        def today_schedule(user) -> str:
            day = datetime.datetime.today().weekday() + 1
            is_odd_week = datetime.datetime.today().isocalendar().week % 2 == 1
            return self.schedule.day_schedule(day, user.group_id, is_odd_week)

        def calendar_day_schedule(user) -> str:
            year, month, day = user.calendar_day.split('/')
            date = datetime.date(int(year), int(month), int(day))
            weekday = date.weekday() + 1
            is_odd_week = date.isocalendar().week % 2 == 1
            return self.schedule.day_schedule(weekday, user.group_id, is_odd_week)

        # main_menu.day_menu init
        self.today_button = LeafButton(
            'Today', 'today', self.day_menu,
            today_schedule, 'group_id'
        )
        self.tomorrow_button = LeafButton('Tomorrow', 'tomorrow', self.day_menu)
        self.calendar_day_button = LeafButton(
            'Calendar Day', 'calendar_day_button', self.day_menu,
            calendar_day_schedule, 'group_id', 'calendar_day'
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
            'Even Week Day', 'even_week_day', self.week_day_menu, lambda n: 'test'
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
        self._update_menu(self.main_menu.callback, '', message.chat_id)
        self.main_menu.operation(
            message,
            self.main_menu.callback,
            User(
                self.user_db.sql_conn,
                message.chat_id
            )
        )


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
        callback_list = query.data.split(';')

        command_str_list = list(filter(
                lambda str_: '!' not in str_ and '=' not in str_ and str_ != '',
                callback_list
        ))
        command_str = command_str_list[0]

        update_strs = [update for update in callback_list if '!' in update]
        new_val_strs = [new_val for new_val in callback_list if '=' in new_val]

        menu_history_str, current_menu = self.user_db.menu_data(update.effective_chat.id)
        menu_history = (menu_history_str or '').split(';')

        if new_val_strs:
            self._new_val_handler(new_val_strs, update)

        user_info = User(self.user_db.sql_conn, update.effective_chat.id)

        if update_strs:
            self._update_handler(
                update_strs, command_str, menu_history, current_menu, query, user_info
            )
        else:
            current_menu = self._default_handler(
                command_str, query, menu_history, user_info, current_menu
            )
        menu_history_str = ';'.join(menu_history)
        self._update_menu(current_menu, menu_history_str, update.effective_chat.id)


    def _default_handler(
        self,
        command_str: str, query: CallbackQuery, menu_history: List[str],
        user_info: User, current_menu: str
    ):
        """
        Handles callbacks that weren't handled by update or new val handlers,
        these are either built-in callbacks or menu buttons
        """
        if command_str == 'pass':
            pass
        elif command_str == 'exit':
            query.delete_message()
        elif command_str == 'back' and menu_history:
            current_menu = menu_history.pop()
            self.main_menu.operation(
                query.message, current_menu, user_info
            )
        elif command_str == 'next_page' and self.current_updater is not None:
            self.current_updater.current_page += 1
            self.current_updater.operation(
                query.message, command_str, user_info
            )
        elif command_str == 'prev_page' and self.current_updater is not None:
            self.current_updater.current_page -= 1
            self.current_updater.operation(
                query.message, command_str, user_info
            )
        elif self.main_menu.operation(
            query.message, command_str, user_info
        ):
            menu_history.append(current_menu)
            current_menu = command_str
        return current_menu


    def _update_menu(self, current_menu, menu_history, id_):
        self.user_db.update_menu(current_menu, menu_history, id_)


    def _new_val_handler(self, new_val_strs: List[str], update: Update):
        for new_val_str in new_val_strs:
            varname, new_val = new_val_str.split('=')
            varname = varname.upper()

            if not new_val.isdigit():
                new_val = "'" + new_val + "'"
            self.user_db.update_or_replace(varname, update.effective_chat.id, new_val)


    def _update_handler(
        self,
        update_strs: List[str],
        command_str: str,
        menu_history: List[str],
        current_menu: str,
        query: CallbackQuery,
        user_info: User
    ):
        upd = update_strs[0]
        update_strs.remove(upd)
        upd = upd.replace('!', '')
        callback = ';'.join(update_strs) + ';' + command_str
        opts = []
        if upd == 'group_id':
            rows = self.schedule_db.execute("""SELECT DISTINCT GROUP_ID
                FROM SCHEDULE""")

            for row in rows:
                id_ = row[0]
                opts.append((id_, id_))
            self.current_updater = MultiPageMenu(
                opts, upd.upper(), callback, True
            )
        elif upd == 'teacher_id':
            pass# TODO
        elif upd == 'student_id':
            pass# TODO
        elif upd == 'calendar_day':
            today = datetime.date.today()
            next_year = datetime.date(today.year + 1, today.month, today.day)
            self.current_updater = CalendarMenu(
                today,
                next_year,
                True,
                callback
            )
        elif upd == 'week_day':
            pass# TODO
        if current_menu not in menu_history:
            menu_history.append(current_menu)
        self.current_updater.operation(query.message, None, user_info)
