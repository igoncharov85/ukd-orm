from enum import Enum


class CheckInStatus(Enum):
    Present = 'Present'
    Absent = 'Absent'
    Empty = 'Empty'


class AssociationStatus(Enum):
    Active = 'Active'
    Archived = 'Archived'
    Deleted = 'Deleted'
