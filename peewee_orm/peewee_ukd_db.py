from datetime import datetime
from peewee import *
import peewee_plus

from ukd_enums import *

db = SqliteDatabase(':memory:')
# db = SqliteDatabase('file.db')


class DbModel(Model):
    class Meta:
        database = db


class UserData(DbModel):
    Login = CharField()
    PasswordHash = CharField(null=True)
    PasswordSalt = CharField(null=True)
    HashAlgo = CharField(null=True)
    ConfirmationToken = CharField(null=True)
    ConfirmationTokenTime = DateTimeField(null=True)
    EmailValidationStatus = BooleanField()
    RecoveryToken = CharField(null=True)
    RecoveryTokenTime = DateTimeField(null=True)


class ExpiredToken(DbModel):
    Token = CharField()
    ExpiresAt = DateTimeField()
    UserData = ForeignKeyField(UserData)


class Teacher(DbModel):
    FirstName = CharField()
    LastName = CharField()
    PhoneNumber = CharField()
    AddressLine1 = CharField()
    City = CharField()
    State = CharField()
    PostalCode = CharField()
    Country = CharField()

    UserData = ForeignKeyField(UserData, backref='Teacher', unique=True)


class Student(DbModel):
    FirstName = CharField()
    LastName = CharField()
    PhoneNumber = CharField(null=True)
    AddressLine1 = CharField(null=True)
    City = CharField(null=True)
    State = CharField(null=True)
    PostalCode = CharField(null=True)
    Country = CharField(null=True)

    UserData = ForeignKeyField(UserData, backref='Student', unique=True)


class TutorStudentAssociation(DbModel):
    Teacher = ForeignKeyField(Teacher, backref='Students')
    Student = ForeignKeyField(Student)
    CreateDateTime = DateTimeField(default=datetime.now())
    Status = peewee_plus.EnumField(AssociationStatus, default=AssociationStatus.Active)

    class Meta:
        primary_key = CompositeKey('Teacher', 'Student')


class Location(DbModel):
    Url = CharField(null=True)
    LocationType = peewee_plus.EnumField(LocationType)
    AddressLine = CharField(null=True)
    City = CharField(null=True)
    State = CharField(null=True)
    PostalCode = CharField(null=True)
    Country = CharField(null=True)

    Tutor = ForeignKeyField(Teacher, backref='Locations', null=True)


class Room(DbModel):
    Name = CharField()
    Capacity = IntegerField()

    Location = ForeignKeyField(Location, backref='Rooms')


class Class(DbModel):
    Name = CharField()
    Status = peewee_plus.EnumField(ClassStatus, default=ClassStatus.Scheduled)
    ClassType = CharField(null=True)
    StartDate = DateField()
    EndScheduleType = peewee_plus.EnumField(ScheduleType)
    EndDate = DateField(null=False)
    EndNumber = IntegerField(null=True)
    MakeupRequired = BooleanField()
    TrackPrepayment = BooleanField()

    Location = ForeignKeyField(Location, null=True)

    Tutor = ForeignKeyField(Teacher, backref='Classes')


class Slot(DbModel):
    SlotUid = UUIDField(primary_key=True)
    DayOfWeek = IntegerField()
    StartTime = TimeField()
    Duration = IntegerField()

    Class = ForeignKeyField(Class, backref='Slots')


class Session(DbModel):
    StartDateTime = DateTimeField()
    Duration = IntegerField()

    Slot = ForeignKeyField(Slot, backref='Sessions')
    Class = ForeignKeyField(Class, backref='Sessions')
    Location = ForeignKeyField(Location, null=True)
    Room = ForeignKeyField(Room, null=True)
    SchoolTeacher = ForeignKeyField(Teacher, null=True)


class Enrollment(DbModel):
    StartDate = DateTimeField()
    EndDate = DateTimeField()
    Notes = CharField()

    Student = ForeignKeyField(Student, backref='Enrollments')
    Class = ForeignKeyField(Class, backref='Enrollments')

    class Meta:
        primary_key = CompositeKey('Student', 'Class')


class CheckIn(DbModel):
    CheckInStatus = peewee_plus.EnumField(CheckInStatus)
    TimeStamp = DateTimeField(default=datetime.now())

    Student = ForeignKeyField(Student, backref='CheckIns')
    Session = ForeignKeyField(Session, backref='CheckIns')


# School

class School(db.Model):
    BusinessName = CharField()
    PhoneNumber = CharField()
    AddressLine1 = CharField()
    City = CharField()
    State = CharField()
    PostalCode = CharField()
    Country = CharField()

    Owner = ForeignKeyField(Teacher)


class SchoolTeacherAssociation(db.Model):
    FirstName = CharField()
    LastName = CharField()
    Email = CharField()
    PhoneNumber = CharField()

    Permission = peewee_plus.EnumField(SchoolPermissionType)
    Notes = CharField(null=True)

    School = ForeignKeyField(School)
    Teacher = ForeignKeyField(Teacher)

    class Meta:
        primary_key = CompositeKey('School', 'Teacher')


class SchoolStudentAssociation(DbModel):
    School = ForeignKeyField(School, backref='Students')
    Student = ForeignKeyField(Student)

    CreateDateTime = DateTimeField(default=datetime.now())
    Status = peewee_plus.EnumField(AssociationStatus, default=AssociationStatus.Active)

    class Meta:
        primary_key = CompositeKey('School', 'Student')


class SchoolClass(db.Model):
    School = ForeignKeyField(School, backref='Classes')
    Class = ForeignKeyField(Class)

    Teacher = ForeignKeyField(Teacher, null=True)

    class Meta:
        primary_key = CompositeKey('School', 'Class')


model_tables = DbModel.__subclasses__()
