import datetime
import pytz

import peewee
from peewee import *

db = SqliteDatabase(':memory:')
print(peewee.__version__)


class DateTimeFieldWithoutTZ(DateTimeField):
    field_type = 'DATETIME'

    def __remove_time_zone(self, value: datetime) -> datetime:
        if value:
            if value.tzinfo:
                return value.replace(tzinfo=None)
            return value

    def db_value(self, value: datetime) -> datetime:
        return self.__remove_time_zone(value)

    def python_value(self, value: datetime) -> datetime:
        return self.__remove_time_zone(value)


class DbModel(Model):
    class Meta:
        database = db


class UserData(DbModel):
    UserId = AutoField(primary_key=True)
    Login = CharField()
    DateTimeWithTZ = DateTimeFieldWithoutTZ()
    DateTimeNoTz = DateTimeField()


class Teacher(DbModel):
    SchoolName = CharField()
    UserData = ForeignKeyField(UserData, backref='Teacher', primary_key=True, object_id_name='TeacherId')


class Student(DbModel):
    University = CharField()
    UserData = ForeignKeyField(UserData, backref='Student', primary_key=True, object_id_name='StudentId')


UserData.Teacher = peewee.BackrefAccessor(Teacher.UserData)
UserData.Student = peewee.BackrefAccessor(Student.UserData)


def main():
    db.create_tables([UserData, Teacher, Student])

    with db.atomic():
        #now_with_tz = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        #assert now_with_tz.tzinfo is not None

        now_with_tz = datetime.datetime.utcnow()

        now_without_tz = datetime.datetime.utcnow()

        user_data = UserData.create(Login='user_login', DateTimeWithTZ=now_with_tz, DateTimeNoTz=now_without_tz)
        teacher = Teacher.create(SchoolName='School1', UserData=user_data)
        student = Student.create(University='University1', UserData=user_data)
        user_data.save()
        teacher.save()
        student.save()

    assert user_data.UserId == student.StudentId
    assert user_data.Student == student
    assert user_data.UserId == teacher.TeacherId
    assert user_data.Teacher == teacher

    with db.atomic():
        first = UserData.select().first()

        print(f'{type(first.DateTimeNoTz)} - {first.DateTimeNoTz}')
        assert first.DateTimeNoTz.tzinfo is None

        print(f'{type(first.DateTimeWithTZ)} - {first.DateTimeWithTZ}')
        #assert first.DateTimeWithTZ.tzinfo is not None


if __name__ == '__main__':
    main()
