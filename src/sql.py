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

cursor = conn.execute("SELECT CLASS_ID, NAME, LECTURER_ID from CLASS")
for row in cursor:
    class_id = row[0]
    class_name = row[1]
    lecturer_id = row[2]

    print("CLASS_ID =", class_id)

    if lecturer_id is not None:
        name = next(conn.execute('''SELECT FIRSTNAME, LASTNAME
        from TEACHER
        where TEACHER_ID = ''' + str(lecturer_id) + '\n'))
        print("Lecturer = " + name[0] + " " + name[1])

    print("NAME =",  class_name, '\n')

conn.close()
