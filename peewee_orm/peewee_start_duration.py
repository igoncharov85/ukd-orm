from datetime import datetime
import peewee
from peewee import *

db = SqliteDatabase(':memory:')
print(peewee.__version__)


class Class(Model):
    ClassId = AutoField(primary_key=True)

    StartDateTime = DateTimeField()
    Duration = IntegerField()


def main():
    start = datetime
    class0 = Class.create(StartDateTime=datetime.now())


if __name__ == '__main__':
    main()
