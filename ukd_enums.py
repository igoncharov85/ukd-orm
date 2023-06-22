from enum import Enum


class CheckInStatus(Enum):
    Present = 'Present'
    Absent = 'Absent'
    Empty = 'Empty'
