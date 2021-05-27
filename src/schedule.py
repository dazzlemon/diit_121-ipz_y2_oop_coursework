"""
Read only manager for schedule database
"""
from itertools import cycle, dropwhile, takewhile
from sqlite3   import Connection

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


    def current_class(self, day: int, hour: int, minute: int, is_odd_week=None):
        #TODO
        pass


    def teacher_info(self, id_):
        """Stringified info about teacher by their id"""
        row = next(self.sql_conn.execute(
            f"""SELECT FIRSTNAME, LASTNAME
               FROM TEACHER
               WHERE TEACHER_ID = {id_}"""
        ))
        result =  f'{row[0]} {row[1]}' + '\n'
        rows = self.sql_conn.execute(
            f"""SELECT NAME,
                      LECTURER_ID,
                      INSTRUCTOR1_ID,
                      INSTRUCTOR2_ID
            FROM CLASS
            WHERE LECTURER_ID = {id_} OR
                  INSTRUCTOR1_ID = {id_} OR
                  INSTRUCTOR2_ID = {id_}"""
        )

        for row in rows:
            subresult = ''
            classname = row[0]
            lecturer_id = row[1]
            ins1_id = row[2]
            ins2_id = row[3]

            if lecturer_id == id_:
                subresult += 'is lecturer'
            if ins1_id == id_ or ins2_id == id_:
                if subresult != '':
                    subresult += ' and instructor'
                else:
                    subresult += 'is instructor'
            subresult += f' for "{classname}"'
            result += subresult + '\n'
        return result


    def class_info(self, id_):
        """Stringified info about class by id"""
        return f'info about class with id={id_}'#TODO


    def group_list(self, id_, subgroup):
        #TODO
        return f'group {id_}'
