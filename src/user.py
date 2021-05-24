"""
user dataclass
"""

from sqlite3 import Connection

class User:
    """
    Easier access to user specific data(args for commands)
    """
    def __init__(self, sql_conn: Connection, id_: int):
        row = next(sql_conn.execute("""SELECT GROUP_ID,
                                              TEACHER_ID,
                                              STUDENT_ID,
                                              CALENDAR_DAY,
                                              WEEK_DAY
                                  FROM USER
                                  WHERE ID = %s""" % id_
        ))
        self.group_id = row[0]
        self.teacher_id = row[1]
        self.student_id = row[2]
        self.calendar_day = row[3]
        self.week_day = row[4]
