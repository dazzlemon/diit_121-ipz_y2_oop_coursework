"""
user dataclass
"""

from dataclasses import dataclass

@dataclass
class User:
    """
    Easier access to user specific data(args for commands)
    """
    group_id: int
    teacher_id: int
    student_id: int
    calendar_day: str
    week_day: int
