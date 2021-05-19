# import sqlite3

# conn = sqlite3.connect('test.db')
# print("Opened database successfully")

# cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
# for row in cursor:
#     print("ID = ", row[0])
#     print("NAME = ", row[1])
#     print("ADDRESS = ", row[2])
#     print("SALARY = ", row[3], "\n")

# print("Operation done successfully")
# conn.close()



class Schedule:
    def __init__(self, group, sql_conn):
        self.group = group
        self.sql_conn = sql_conn

    def odd_week_schedule(self):
        for day in range(1, 6):
            cursor = conn.execute(
                '''SELECT TIME, IS_LECTURE, CLASS_ID
                from SCHEDULE
                where DAY = ''' + str(day) +
                ' AND (ODD_WEEK = 1 OR ODD_WEEK IS NULL) AND GROUP_ID = '
                + str(self.group) + ' ORDER BY TIME'
            )

            day_str = None

            if day == 1:
                day_str = 'MONDAY'
            elif day == 2:
                day_str = 'TUESDAY'
            elif day == 3:
                day_str = 'WEDNESDAY'
            elif day == 4:
                day_str = 'THURSDAY'
            elif day == 5:
                day_str = 'FRIDAY'

            print(day_str)

            for row in cursor:
                time = row[0]
                is_lecture = row[1]
                class_id = row[2]

                classname = next(
                    conn.execute(
                        'SELECT NAME from CLASS where CLASS_ID = '
                        + str(class_id)
                    )
                )[0]

                print(f"{'lecture' if is_lecture else 'practice'} about '{classname}' at {time}")
            print()

if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('schedule.db')

    s = Schedule(911, conn)
    s.odd_week_schedule()

    conn.close()
