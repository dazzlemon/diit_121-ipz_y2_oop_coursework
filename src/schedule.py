"""
Read only manager for schedule database
"""
from itertools import cycle, dropwhile, takewhile
from sqlite3   import Connection
from user      import User

class Schedule:
    """
    Read only manager for schedule database
    """
    def __init__(self, sql_conn: Connection):
        self.sql_conn = sql_conn


    def week_schedule(self, group_id: int, is_odd_week=None):
        """
        schedule for week, whole/odd/even
        """
        result = ''
        for day in range(1, 6):
            result += self.day_schedule(day, group_id, is_odd_week) + '\n'
        return result


    def day_schedule(self, day: int, group_id: int, is_odd_week=None):
        """
        schedule for day, whole/odd/even
        """
        odd_week_str = 'Whole week'
        if is_odd_week is not None:
            odd_week_str = 'Odd week' if is_odd_week else 'Even week'
        result = self.day_from_int(day) + f'({odd_week_str})' + '\n'
        for row in self._day_schedule(day, group_id, is_odd_week):
            time = row[0]
            is_lecture = row[1]
            class_id = row[2]
            class_odd_week = row[3]

            classname = next(
                self.sql_conn.execute(
                    'SELECT NAME from CLASS where CLASS_ID = '
                    + str(class_id)
                )
            )[0]

            type_ = 'lecture' if is_lecture else 'practice'
            result += f'{time} - "{classname}"; {type_}'
            if is_odd_week is None and class_odd_week is not None:
                result += f'({"Odd" if class_odd_week == 1 else "Even"})'
            result += '\n'
        return result + '\n'


    def _day_schedule(self, day: int, group_id: int, is_odd_week=None):
        week_constraint = ''
        if is_odd_week is not None:
            boolean = 1 if is_odd_week else 0
            week_constraint = f'AND (ODD_WEEK = {boolean} OR ODD_WEEK IS NULL)'

        return self.sql_conn.execute(
            '''SELECT TIME, IS_LECTURE, CLASS_ID, ODD_WEEK
            from SCHEDULE
            where DAY = %s
            %s AND GROUP_ID = %s
            ORDER BY TIME''' % (
                day,
                week_constraint,
                group_id
            )
        )


    @staticmethod
    def day_from_int(day: int):
        """returns string with day name from int"""
        days = [
            '',# 1 based
            'MONDAY',
            'TUESDAY',
            'WEDNESDAY',
            'THURSDAY',
            'FRIDAY',
            'SATURDAY',
            'SUNDAY',
        ]
        return days[day]


    def next_class(self, day: int, hour: int, minute: int, is_odd_week=None):
        """day, hour, minute is <current_time>"""
        if 1 <= day <= 7:
            counter = 0
            def count(_):
                nonlocal counter
                counter += 1
                return counter <= 7

            for day_ in takewhile(
                count,
                dropwhile(lambda n: n < day, cycle(range(1, 8)))
            ):
                # check one week forward(8th day is the same as today)
                for row in self._day_schedule(day_, is_odd_week):
                    time = row[0]
                    is_lecture = row[1]
                    class_id = row[2]

                    time_hour, time_min = time.split(':')
                    time_hour = int(time_hour)
                    time_min = int(time_min)

                    if (
                        (time_hour == hour and time_min > minute)
                        or time_hour > hour
                    ):
                        classname = next(
                            self.sql_conn.execute(
                                'SELECT NAME from CLASS where CLASS_ID = '
                                + str(class_id)
                            )
                        )[0]

                        is_lecture_str = "lecture" if is_lecture else "practice"

                        return ('Your next class is %s(%s)\n' % (
                                classname,
                                is_lecture_str
                            ) + f'on {self.day_from_int(day_)}, at {time}'
                        )


    def teacher_info(self, user: User):
        row = next(self.sql_conn.execute(
            f"""SELECT FIRSTNAME, LASTNAME
               FROM TEACHER
               WHERE TEACHER_ID = {user.teacher_id}"""
        ))
        return f'Info about {row[0]} {row[1]}'#TODO


    def class_info(self, user: User):
        return f'info about class with id={user.class_id}'#TODO
