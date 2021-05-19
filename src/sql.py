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

import sqlite3

conn = sqlite3.connect('schedule.db')

cursor = conn.execute(
    '''SELECT CLASS_ID,
              NAME,
              LECTURER_ID,
              INSTRUCTOR1_ID,
              INSTRUCTOR2_ID,
              LECTURE_ROOM_ID,
              ROOM1_ID,
              ROOM2_ID
from CLASS'''
)
# for row in cursor:
#     class_id = row[0]
#     class_name = row[1]
#     lecturer_id = row[2]
#     instructor1_id = row[3]
#     instructor2_id = row[4]
#     lecture_room = row[5]
#     room1 = row[6]
#     room2 = row[7]

#     print("class =", class_name)

#     if lecturer_id is not None:
#         name = next(conn.execute('''SELECT FIRSTNAME, LASTNAME
#         from TEACHER
#         where TEACHER_ID = ''' + str(lecturer_id) + '\n'))
#         print("Lecturer = " + name[0] + " " + name[1])
#     else:
#         print('lecturer not specified')

#     if instructor1_id is not None:
#         name = next(conn.execute('''SELECT FIRSTNAME, LASTNAME
#         from TEACHER
#         where TEACHER_ID = ''' + str(lecturer_id) + '\n'))
#         print("instructor1 = " + name[0] + " " + name[1])
#     else:
#         print('instructor1 not specified')

#     if instructor2_id is not None:
#         name = next(conn.execute('''SELECT FIRSTNAME, LASTNAME
#         from TEACHER
#         where TEACHER_ID = ''' + str(lecturer_id) + '\n'))
#         print("instructor2 = " + name[0] + " " + name[1])
#     else:
#         print('instructor2 not specified')

#     print('\n')

for day in range(1, 6):
    cursor = conn.execute(
        '''SELECT TIME, IS_LECTURE, CLASS_ID
        from SCHEDULE
        where DAY = ''' + str(day) + ' AND (ODD_WEEK = 1 OR ODD_WEEK IS NULL) AND GROUP_ID = 911' +
        ' ORDER BY TIME'
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

        classname = next(conn.execute('SELECT NAME from CLASS where CLASS_ID = ' + str(class_id)))[0]

        print(f"{'lecture' if is_lecture else 'practice'} about '{classname}' at {time}")
    print()

conn.close()
