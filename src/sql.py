from itertools import cycle, dropwhile, takewhile
from sqlite3 import Connection

class Schedule:
    def __init__(self, sql_conn: Connection):
        self.sql_conn = sql_conn


    def week_schedule(self, group_id: int, is_odd_week=None):
        result = ''
        for day in range(1, 6):
            result += self.day_from_int(day) + '\n'
            result += self.day_schedule(day, group_id, is_odd_week) + '\n'
        return result


    def day_schedule(self, day: int, group_id: int, is_odd_week=None):
        odd_week_str = 'Odd week' if is_odd_week else 'Even week'
        result = self.day_from_int(day) + f'({odd_week_str})' + '\n'
        for row in self._day_schedule(day, group_id, is_odd_week):
            time = row[0]
            is_lecture = row[1]
            class_id = row[2]

            classname = next(
                self.sql_conn.execute(
                    'SELECT NAME from CLASS where CLASS_ID = '
                    + str(class_id)
                )
            )[0]

            type_ = 'lecture' if is_lecture else 'practice'
            result += f'{time} - "{classname}"; {type_}' + '\n'
        return result + '\n'


    def _day_schedule(self, day: int, group_id: int, is_odd_week=None):
        week_constraint = ''
        if is_odd_week is not None:
            boolean = 1 if is_odd_week else 0
            week_constraint = f'AND (ODD_WEEK = {boolean} OR ODD_WEEK IS NULL)'

        return self.sql_conn.execute(
            '''SELECT TIME, IS_LECTURE, CLASS_ID
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
    def day_from_int(day):
        if day == 1:
            return 'MONDAY'
        elif day == 2:
            return 'TUESDAY'
        elif day == 3:
            return 'WEDNESDAY'
        elif day == 4:
            return 'THURSDAY'
        elif day == 5:
            return 'FRIDAY'
        elif day == 6:
            return 'SATURDAY'
        elif day == 7:
            return 'SUNDAY'


    def next_class(self, day, hour, minute, is_odd_week=None):
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

                        return (f'Your next class is {classname}({"lecture" if is_lecture else "practice"})' + '\n' +
                            f'on {self.day_from_int(day_)}, at {time}')


if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('schedule.db')

    s = Schedule(conn)
    print(s.week_schedule(911, True))

    print(s.next_class(911, 1, 8, 1))

    conn.close()
