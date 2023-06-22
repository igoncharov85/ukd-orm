from peewee import *
import peewee_plus

from ukd_enums import *

db = SqliteDatabase(':memory:')
# db = SqliteDatabase('file.db')


class BaseModel(Model):
    class Meta:
        database = db


class UserData(BaseModel):
    Login = CharField()
    PasswordHash = CharField()
    PasswordSalt = CharField()
    HashAlgo = CharField()
    ConfirmationToken = CharField()
    ConfirmationTokenTime = DateTimeField()
    EmailValidationStatus = BooleanField()
    RecoveryToken = CharField()
    RecoveryTokenTime = DateTimeField()


class ExpiredToken(BaseModel):
    Token = CharField()
    ExpiresAt = DateTimeField()
    UserData = ForeignKeyField(UserData)


class Teacher(BaseModel):
    FirstName = CharField()
    LastName = CharField()
    PhoneNumber = CharField()
    AddressLine1 = CharField()
    City = CharField()
    State = CharField()
    PostalCode = CharField()
    Country = CharField()

    UserData = ForeignKeyField(UserData, backref='Teacher', unique=True)

    # AssociatedStudents = relationship('Student', secondary=tutor_associated_students)
    # TutorLocations = relationship('Location', secondary=tutor_locations)
    # TutorClasses = relationship('Class', secondary=tutor_classes, back_populates='Tutor')

    #UserData: Mapped[UserData] = relationship(UserData, uselist=False)


class Student(BaseModel):
    FirstName = CharField()
    LastName = CharField()
    PhoneNumber = CharField()
    AddressLine1 = CharField()
    City = CharField()
    State = CharField()
    PostalCode = CharField()
    Country = CharField()

    UserData = ForeignKeyField(UserData, backref='Student', unique=True)

    # Enrollments = relationship('Enrollment', back_populates='Student')


class Location(BaseModel):
    Url = CharField()
    LocationType = CharField()
    AddressLine = CharField(null=True)
    City = CharField(null=True)
    State = CharField(null=True)
    PostalCode = CharField(null=True)
    Country = CharField(null=True)

    Tutor = ForeignKeyField(Teacher, backref='Locations', null=True)
    # School: Mapped['School'] = relationship('School', secondary=school_locations, back_populates='Locations', uselist=False)

    # Rooms: Mapped[List['Room']] = relationship('Room')


class Room(BaseModel):
    Name = CharField()
    Capacity = IntegerField()

    Location = ForeignKeyField(Location, backref='Rooms')


class Class(BaseModel):
    Name = CharField()
    Status = CharField()
    ClassType = CharField(null=True)
    StartDate = DateField()
    EndScheduleType = CharField()
    EndDate = DateField(null=False)
    EndNumber = IntegerField(null=True)
    MakeupRequired = BooleanField()
    TrackPrepayment = BooleanField()

    Location = ForeignKeyField(Location, null=True)

    #Enrollments = relationship('Enrollment', back_populates='Class')

    #Tutor = relationship(Teacher, secondary=tutor_classes, back_populates='TutorClasses', uselist=False)


class Slot(BaseModel):
    uid = UUIDField(primary_key=True)
    DayOfWeek = IntegerField()
    StartTime = TimeField()
    Duration = IntegerField()

    Class = ForeignKeyField(Class, backref='Slots')


class Session(BaseModel):
    StartDateTime = DateTimeField()
    Duration = IntegerField()

    Slot = ForeignKeyField(Slot, backref='Sessions')
    Class = ForeignKeyField(Class, backref='Sessions')
    Location = ForeignKeyField(Location, null=True)
    Room = ForeignKeyField(Room, null=True)
    SchoolTeacher = ForeignKeyField(Teacher, null=True)


class Enrollment(BaseModel):
    StartDate = DateTimeField()
    EndDate = DateTimeField()
    Notes = CharField()

    Student = ForeignKeyField(Student, backref='Enrollments')
    Class = ForeignKeyField(Class, backref='Enrollments')

    class Meta:
        primary_key = CompositeKey('Student', 'Class')


class CheckIn(BaseModel):
    CheckInStatus = peewee_plus.EnumField(CheckInStatus)
    TimeStamp = DateTimeField()

    Student = ForeignKeyField(Student, backref='CheckIns')
    Session = ForeignKeyField(Session, backref='CheckIns')
