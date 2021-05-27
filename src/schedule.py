"""
Read only manager for schedule database
"""
import datetime
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


    def next_class(
        self, day: int, hour: int, minute: int, group_id, is_odd_week=None
    ):
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
                for row in self._day_schedule(day_, group_id, is_odd_week):
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
        return f'There is no schedule for {group_id}!'


    def current_class(
        self, day: int, hour: int, minute: int, group_id: int, is_odd_week=None
    ):
        """returns stringified info about current class
        day, hour, minute is <current_time>"""
        if 1 <= day <= 7:
            for row in self._day_schedule(day, group_id, is_odd_week):
                time = row[0]
                is_lecture = row[1]
                class_id = row[2]

                time_hour, time_min = time.split(':')
                time_hour = int(time_hour)
                time_min = int(time_min)

                time_now = datetime.time(hour, minute)
                time_class_start = datetime.time(time_hour, time_min)
                time_class_finish = time_class_start + datetime.timedelta(
                    minutes=80
                )

                if time_class_start < time_now < time_class_finish:
                    classname = next(
                        self.sql_conn.execute(
                            'SELECT NAME from CLASS where CLASS_ID = '
                            + str(class_id)
                        )
                    )[0]

                    is_lecture_str = "lecture" if is_lecture else "practice"

                    return ('Your next current class is %s(%s)\n' % (
                            classname,is_lecture_str
                    ))
            return "You don't have a class rigth now"


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
        row = next(self.sql_conn.execute(
            f"""SELECT NAME,
                      LECTURER_ID,
                      INSTRUCTOR1_ID,
                      INSTRUCTOR2_ID,
                      LECTURE_ROOM_ID,
                      ROOM1_ID,
                      ROOM2_ID
            FROM CLASS
            WHERE CLASS_ID = {id_}"""
        ))
        name = row[0]
        lecturer_id = row[1]
        ins1_id = row[2]
        ins2_id = row[3]
        lec_room = row[4]
        room1 = row[5]
        room2 = row[6]

        lecturer = next(self.sql_conn.execute(
            f"""SELECT FIRSTNAME, LASTNAME
            FROM TEACHER
            WHERE TEACHER_ID = {lecturer_id}"""
        ))
        ins1 = next(self.sql_conn.execute(
            f"""SELECT FIRSTNAME, LASTNAME
            FROM TEACHER
            WHERE TEACHER_ID = {ins1_id}"""
        ))
        ins2 = None
        if ins2_id is not None:
            ins2 = next(self.sql_conn.execute(
                f"""SELECT FIRSTNAME, LASTNAME
                FROM TEACHER
                WHERE TEACHER_ID = {ins2_id}"""
            ))

        result = ''
        result += name + '\n'
        result += f'lecturer: {lecturer[0]} {lecturer[1]}' + '\n'
        result += f'instructor 1: {ins1[0]} {ins1[1]}' + '\n'
        if ins2 is not None:
            result += f'instructor 2: {ins2[0]} {ins2[1]}' + '\n'
        result += f'lecture room: {lec_room}' + '\n'
        result += f'room 1: {room1}' + '\n'
        if room2 is not None:
            result += f'room 2: {room2}' + '\n'
        return result


    def group_list(self, id_: int, subgroup: int=None):
        """stringified list group"""
        subgroup_constraint = ''
        if subgroup is not None:
            subgroup_constraint = f' AND SUBGROUP = {subgroup}'
        rows = self.sql_conn.execute(
            f"""SELECT FIRSTNAME,
                       LASTNAME,
                       SUBGROUP
                FROM STUDENT
                WHERE GROUP_ID = {id_}""" + subgroup_constraint)

        result = ''
        for row in rows:
            name = row[0] + ' ' + row[1]
            subgr = row[2]

            result += name
            if subgroup is None:
                result += f'(subgroup: {subgr})'
            result += '\n'
        if result != '':
            return result
        else:
            return 'NO STUDENTS FOUND'
