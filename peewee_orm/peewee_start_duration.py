from datetime import datetime, timedelta
import peewee
from peewee import *
from playhouse.db_url import connect
from playhouse.hybrid import hybrid_property

#db = SqliteDatabase(':memory:')
db = connect('mysql://')
print(peewee.__version__)


class Session(Model):
    SessionId = AutoField(primary_key=True)

    StartDateTime = DateTimeField()
    Duration = IntegerField()

    @hybrid_property
    def EndDateTime(self):
        return self.StartDateTime + timedelta(minutes=self.Duration)

    @EndDateTime.expression
    def EndDateTime(cls):
        end = SQL(f'DATE_ADD({cls.StartDateTime}, INTERVAL {cls.Duration} MINUTE)', [cls.StartDateTime, cls.Duration])
        return end

    class Meta:
        database = db


db.create_tables([Session])


def main():
    now = datetime.now()
    in_an_hour = now + timedelta(hours=1)
    with db.atomic():
        Session.create(StartDateTime=now, Duration=10)
        Session.create(StartDateTime=now, Duration=10)
        Session.create(StartDateTime=in_an_hour, Duration=10)
    assert len(Session) == 3
    for session in Session:
        print(f'{session.SessionId}={session.Duration} - {session.StartDateTime} - {session.EndDateTime}')

    for session in Session.select().where(Session.EndDateTime <= in_an_hour):
        print(f'{session.SessionId} - {session.StartDateTime} - {session.EndDateTime}')


if __name__ == '__main__':
    main()
