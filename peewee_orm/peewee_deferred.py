import peewee
from peewee import *

db = SqliteDatabase(':memory:')
print(peewee.__version__)


class DbModel(Model):
    class Meta:
        database = db


class UserData(DbModel):
    UserId = AutoField(primary_key=True)
    Login = CharField()


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
        user_data = UserData.create(Login='user_login')
        teacher = Teacher.create(SchoolName='School1', UserData=user_data)
        student = Student.create(University='University1', UserData=user_data)

    assert user_data.UserId == student.StudentId
    assert user_data.Student == student
    assert user_data.UserId == teacher.TeacherId
    assert user_data.Teacher == teacher


if __name__ == '__main__':
    main()
