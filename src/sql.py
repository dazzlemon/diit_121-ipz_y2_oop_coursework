from itertools import cycle, dropwhile, takewhile

class Schedule:
    def __init__(self, group, sql_conn):
        self.group = group
        self.sql_conn = sql_conn


    def week_schedule(self, is_odd_week=None):
        for day in range(1, 6):
            print(self.day_from_int(day))
            self.day_schedule(day, is_odd_week)


    def day_schedule(self, day, is_odd_week=None):
        for row in self._day_schedule(day, is_odd_week):
            time = row[0]
            is_lecture = row[1]
            class_id = row[2]

            classname = next(
                self.sql_conn.execute(
                    'SELECT NAME from CLASS where CLASS_ID = '
                    + str(class_id)
                )
            )[0]

            print(f"{'lecture' if is_lecture else 'practice'} about '{classname}' at {time}")
        print()


    def _day_schedule(self, day, is_odd_week=None):
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
                self.group
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

                        print(f'Your next class is {classname}({"lecture" if is_lecture else "practice"})')
                        print(f'on {self.day_from_int(day_)}, at {time}')
                        return



if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('schedule.db')

    s = Schedule(911, conn)
    s.week_schedule(True)

    s.next_class(1, 8, 1)

    conn.close()
