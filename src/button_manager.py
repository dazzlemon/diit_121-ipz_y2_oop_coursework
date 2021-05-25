"""
Button manager for timetable bot, using button module
"""

import datetime
from button         import LeafButton, Menu
from user           import User
from multipage_menu import MultiPageMenu
from sql            import Schedule


class ButtonManager:
    """
    Button manager for timetable bot, using button module
    """
    def __init__(self, user_db, schedule_db):
        self.user_db = user_db
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
            day = datetime.datetime.today().weekday()
            is_odd_week = datetime.datetime.today().isocalendar()[1] % 2 == 1
            return self.schedule.day_schedule(day, user.group_id, is_odd_week)

        # main_menu.day_menu init
        self.today_button = LeafButton(
            'Today', 'today', self.day_menu,
            today_schedule, 'group_id'
        )
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
        self.user_db.execute("""REPLACE INTO USER
                (CURRENT_MENU, MENU_HISTORY, ID)
            VALUES
                ('%s', '', %s)""" % (self.main_menu.callback, message.chat_id)
        )
        self.user_db.commit()
        self.main_menu.operation(
            message,
            self.main_menu.callback,
            User(
                self.user_db,
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
        update_strs = list(map(lambda str_: str_.replace('!', ''), update_strs))
        new_val_strs = [new_val for new_val in callback_list if '=' in new_val]

        row = next(self.user_db.execute("""SELECT MENU_HISTORY, CURRENT_MENU
                FROM USER
                WHERE ID = %s""" % update.effective_chat.id))

        menu_history_str = row[0]
        current_menu = row[1]

        menu_history = (menu_history_str or '').split(';')

        if new_val_strs:
            for new_val_str in new_val_strs:
                varname, new_val = new_val_str.split('=')
                varname = varname.upper()

                row = next(self.user_db.execute(
                    """SELECT %s FROM USER""" % varname
                ))
                if row[0] is str:
                    new_val = "'" + new_val + "'"

                self.user_db.execute("""REPLACE INTO USER
                        (ID, %s)
                    VALUES
                        (%s, %s)""" % (
                            varname,
                            update.effective_chat.id,
                            new_val
                        )
                )
                self.user_db.commit()

        user_info = User(self.user_db, update.effective_chat.id)

        if update_strs:
            upd = update_strs[0]
            update_strs.remove(upd)
            callback = ';'.join(update_strs) + ';' + command_str
            opts = []
            if upd == 'group_id':
                rows = self.schedule_db.execute("""SELECT DISTINCT GROUP_ID
                    FROM SCHEDULE""")

                for row in rows:
                    id_ = row[0]
                    opts.append((id_, id_))
            elif upd == 'teacher_id':
                pass# TODO
            elif upd == 'student_id':
                pass# TODO
            elif upd == 'calendar_day':
                pass# TODO
            elif upd == 'week_day':
                pass# TODO
            self.current_updater = MultiPageMenu(opts, upd.upper(), callback, True)
            menu_history.append(current_menu)
            current_menu = upd + '_choice'
            self.current_updater.operation(query.message, None, user_info)
        else:
            if command_str == 'exit':
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
            else:
                if self.main_menu.operation(
                    query.message, command_str, user_info
                ):
                    menu_history.append(current_menu)
                    current_menu = command_str
        menu_history_str = ';'.join(menu_history)
        self.user_db.execute("""REPLACE INTO USER
                (CURRENT_MENU, MENU_HISTORY, ID)
            VALUES
                ('%s', '%s', %s)""" % (
                    current_menu, menu_history_str, update.effective_chat.id
                )
        )
        self.user_db.commit()
