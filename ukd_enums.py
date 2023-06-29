from enum import Enum


class CheckInStatus(Enum):
    Present = 'Present'
    Absent = 'Absent'
    Empty = 'Empty'


class AssociationStatus(Enum):
    Active = 'Active'
    Archived = 'Archived'
    Deleted = 'Deleted'


class LocationType(Enum):
    Online = 'Online'
    Office = 'Office'


class ClassStatus(Enum):
    Scheduled = 'Scheduled'
    Archived = 'Archived'
    Deleted = 'Deleted'


class ScheduleType(Enum):
    SpecificEndDate = 'SpecificEndDate'
    FixedClassesNumber = 'FixedClassesNumber'
    FixedWeekNumber = 'FixedWeekNumber'
    FixedMonthNumber = 'FixedMonthNumber'


class SchoolPermissionType(Enum):
    ViewOwnSchedule = 'ViewOwnSchedule'
    ManageOwnSchedule = 'ManageOwnSchedule'
    ManageSchedule = 'ManageSchedule'
    FullAccess = 'FullAccess'
