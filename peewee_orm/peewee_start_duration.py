from datetime import datetime, timedelta
import peewee
from peewee import *
from playhouse.db_url import connect
from playhouse.hybrid import hybrid_property

db = SqliteDatabase(':memory:')
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
        return cls.StartDateTime.to_timestamp() + cls.Duration

    class Meta:
        database = db


db.create_tables([Session])


def main():
    import pytz
    UTC_TIMEZONE = pytz.timezone('UTC')

    start1 = datetime(2023, 9, 1, 5, 0)
    start2 = datetime(2023, 9, 1, 9, 0)
    if not len(Session):
        with db.atomic():
            Session.create(StartDateTime=start1, Duration=60)
            Session.create(StartDateTime=start1, Duration=60)
            Session.create(StartDateTime=start2, Duration=60)
    assert len(Session) == 3

    print('Sessions:')
    for session in Session:
        print(f'{session.SessionId}: Duration={session.Duration}, StartDateTime={session.StartDateTime} - EndDateTime={session.EndDateTime}')

    print(f'Comparing with {start2}')
    start2 = start2.replace(tzinfo=UTC_TIMEZONE)
    assert Session.select().where(Session.EndDateTime <= start2.timestamp()).order_by(Session.EndDateTime).count() == 2
    assert Session.select().where(Session.EndDateTime >= start2.timestamp()).order_by(Session.EndDateTime).count() == 1


if __name__ == '__main__':
    main()
