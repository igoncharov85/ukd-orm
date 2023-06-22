import uuid
from peewee_orm.peewee_ud_db import *
from datetime import date, time, datetime, timedelta


def create_tables():
    tables = [UserData, ExpiredToken, Teacher, Student, Location, Room, Class, Slot, Session, Enrollment, CheckIn]
    db.drop_tables(tables)
    db.create_tables(tables)


def main():
    create_tables()
    with db.atomic():
        # Teacher
        user_data = UserData.create(Login='igor@goncharov.dev', PasswordHash='Hash', PasswordSalt='Salt', HashAlgo='HashAlgo',
                                    ConfirmationToken='ConfirmationToken', ConfirmationTokenTime=datetime.now(), EmailValidationStatus=True,
                                    RecoveryToken='RecoveryToken', RecoveryTokenTime=datetime.now())
        teacher = Teacher.create(FirstName='Igor', LastName='Goncharov', PhoneNumber='6463732444',
                                 AddressLine1='Add', City='JC', State='NJ', PostalCode='07310', Country='USA', UserData=user_data)
        # Student
        student1_user_data = UserData.create(Login='student1@goncharov.dev', PasswordHash='Hash', PasswordSalt='Salt', HashAlgo='HashAlgo',
                                             ConfirmationToken='ConfirmationToken', ConfirmationTokenTime=datetime.now(), EmailValidationStatus=True,
                                             RecoveryToken='RecoveryToken', RecoveryTokenTime=datetime.now())
        student1 = Student.create(FirstName='Igor', LastName='Goncharov', PhoneNumber='6463732444',
                                            AddressLine1='Add', City='JC', State='NJ', PostalCode='07310', Country='USA', UserData=student1_user_data)
        student2_user_data = UserData.create(Login='student1@goncharov.dev', PasswordHash='Hash', PasswordSalt='Salt', HashAlgo='HashAlgo',
                                             ConfirmationToken='ConfirmationToken', ConfirmationTokenTime=datetime.now(), EmailValidationStatus=True,
                                             RecoveryToken='RecoveryToken', RecoveryTokenTime=datetime.now())
        student2 = Student.create(FirstName='Igor', LastName='Goncharov', PhoneNumber='6463732444',
                                            AddressLine1='Add', City='JC', State='NJ', PostalCode='07310', Country='USA', UserData=student2_user_data)
        # Location
        location = Location.create(Url='https://zoom.us', LocationType='T', Tutor=teacher)
        # Class
        class_item = Class.create(Name='Music', Status='Active', ClassType='ClassType',
                                  StartDate=date(2023, 7, 1), EndScheduleType='Fixed',
                                  EndDate=date(2023, 7, 28), MakeupRequired=True, TrackPrepayment=True, Location=location)
        # Slots
        slot1 = Slot.create(uid=uuid.uuid4(), DayOfWeek=1, StartTime=time(16, 0), Duration=60, Class=class_item)
        slot2 = Slot.create(uid=uuid.uuid4(), DayOfWeek=3, StartTime=time(17, 0), Duration=60, Class=class_item)
        slot3 = Slot.create(uid=uuid.uuid4(), DayOfWeek=5, StartTime=time(18, 0), Duration=60, Class=class_item)
        # Sessions
        t = date.today()
        t1 = t + timedelta(days=7)
        session1 = Session.create(StartDateTime=datetime.combine(t, slot1.StartTime), Duration=slot1.Duration, Slot=slot1, Class=class_item)
        session2 = Session.create(StartDateTime=datetime.combine(t, slot2.StartTime), Duration=slot2.Duration, Slot=slot2, Class=class_item)
        session3 = Session.create(StartDateTime=datetime.combine(t, slot3.StartTime), Duration=slot3.Duration, Slot=slot3, Class=class_item)
        session4 = Session.create(StartDateTime=datetime.combine(t1, slot1.StartTime), Duration=slot1.Duration, Slot=slot1, Class=class_item)
        session5 = Session.create(StartDateTime=datetime.combine(t1, slot2.StartTime), Duration=slot2.Duration, Slot=slot2, Class=class_item)
        session6 = Session.create(StartDateTime=datetime.combine(t1, slot3.StartTime), Duration=slot3.Duration, Slot=slot3, Class=class_item)

        # Enrollment
        start = session1.StartDateTime
        end = session6.StartDateTime+timedelta(minutes=session6.Duration)
        student1_enrollment = Enrollment.create(StartDate=start, EndDate=end, Notes='', Student=student1, Class=class_item)
        student2_enrollment = Enrollment.create(StartDate=start, EndDate=end, Notes='', Student=student2, Class=class_item)

        check_in1 = CheckIn.create(CheckInStatus=CheckInStatus.Present, TimeStamp=datetime.now(), Student=student1, Session=session2)
        check_in2 = CheckIn.create(CheckInStatus=CheckInStatus.Absent, TimeStamp=datetime.now(), Student=student2, Session=session2)

        # user_data.save()
        # teacher.save()
        # location.save()
        # class_item.save()
        print(f'id = {user_data.id}')

    with db:
        t = Teacher.get(Teacher.id == 1)
        for location in t.Locations:
            print(f'{location.id} - {location.Url}')
        for slot in Slot.select():
            print(f'{slot.uid} - {slot.StartTime}')
        print(f'Len(Slots) = {len(Slot.select())}')
        print(f'Len(Session) = {len(Session.select())}')
        print(f'Len(Enrollment) = {len(Enrollment.select())}')

        print(f'Len(CheckIn) = {len(CheckIn.select())}')
        print(f'Len(CheckIn)==Present - {len(CheckIn.select().where(CheckIn.CheckInStatus==CheckInStatus.Present))}')
        print(f'Len(CheckIn)==Absent - {len(CheckIn.select().where(CheckIn.CheckInStatus==CheckInStatus.Absent))}')


    pass


if __name__ == '__main__':
    main()
