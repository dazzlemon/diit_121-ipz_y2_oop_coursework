"""
Manager for user info
"""
from typing import List
from user   import User

class UserDbManager:
    """
    Manager for user info
    """
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn


    def menu_data(self, id_: int):
        """returns tuple (menu_history_str, current_menu)"""
        row = next(self.sql_conn.execute(f"""SELECT MENU_HISTORY, CURRENT_MENU
                FROM USER
                WHERE ID = {id_}"""
        ))
        menu_history_str = row[0]
        current_menu = row[1]
        return menu_history_str, current_menu


    def update_menu(self, current_menu: str, menu_history: List[str], id_: int):
        """inserts or replaces info about users state"""
        menu_history_str = ';'.join(menu_history)
        if self.is_row_exists(id_):
            self.sql_conn.execute(
                f"""UPDATE USER
                    SET CURRENT_MENU = '{current_menu}',
                        MENU_HISTORY = '{menu_history_str}'
                    WHERE ID = {id_}"""
            )
        else:
            self.sql_conn.execute(f"""REPLACE INTO USER
                    (CURRENT_MENU, MENU_HISTORY, ID)
                VALUES
                    ('{current_menu}', '{menu_history_str}', {id_})"""
            )
        self.sql_conn.commit()


    def is_row_exists(self, id_):
        """check if row with id exists"""
        row = next(self.sql_conn.execute(
            f"""SELECT * FROM USER WHERE ID = {id_}"""
        ), None)
        return row is not None


    def insert_or_replace(self, varname: str, id_: int, new_val: str):
        """inserts or updates varname with new_val"""
        print()
        print(varname)
        print(id_)
        print(new_val)
        print()
        if self.is_row_exists(id_):
            self.sql_conn.execute(
                f"""UPDATE USER
                    SET {varname} = {new_val}
                    WHERE ID = {id_}"""
            )
        else:
            self.sql_conn.execute(f"""REPLACE INTO USER
                    (ID, {varname})
                VALUES
                    ({id_}, {new_val})"""
            )
        self.sql_conn.commit()


    def user(self, id_):
        """returns user by their id"""
        row = next(self.sql_conn.execute("""SELECT GROUP_ID,
                                              TEACHER_ID,
                                              STUDENT_ID,
                                              CALENDAR_DAY,
                                              WEEK_DAY
                                  FROM USER
                                  WHERE ID = %s""" % id_
        ))
        return User(row[0], row[1], row[2], row[3], row[4])
