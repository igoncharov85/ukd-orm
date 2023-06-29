import uuid
from peewee_orm.peewee_ukd_db import *
from datetime import date, time, datetime, timedelta


def create_tables():
    db.create_tables(model_tables)


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
        student2_user_data = UserData.create(Login='student2@goncharov.dev', PasswordHash='Hash', PasswordSalt='Salt', HashAlgo='HashAlgo',
                                             ConfirmationToken='ConfirmationToken', ConfirmationTokenTime=datetime.now(), EmailValidationStatus=True,
                                             RecoveryToken='RecoveryToken', RecoveryTokenTime=datetime.now())
        student2 = Student.create(FirstName='Igor', LastName='Goncharov', PhoneNumber='6463732444',
                                  AddressLine1='Add', City='JC', State='NJ', PostalCode='07310', Country='USA', UserData=student2_user_data)

        TutorStudentAssociation.create(Teacher=teacher, Student=student1)
        TutorStudentAssociation.create(Teacher=teacher, Student=student2, Status=AssociationStatus.Archived)

        # Location
        location = Location.create(Url='https://zoom.us', LocationType=LocationType.Online, Tutor=teacher)
        # Class
        class_item = Class.create(Name='Music', Status=ClassStatus.Scheduled, ClassType='ClassType',
                                  StartDate=date(2023, 7, 1), EndScheduleType=ScheduleType.FixedWeekNumber,
                                  EndDate=date(2023, 7, 28), MakeupRequired=True, TrackPrepayment=True, Location=location, Tutor=teacher)
        # Slots count=3
        slot1 = Slot.create(SlotUid=uuid.uuid4(), DayOfWeek=1, StartTime=time(16, 0), Duration=60, Class=class_item)
        slot2 = Slot.create(SlotUid=uuid.uuid4(), DayOfWeek=3, StartTime=time(17, 0), Duration=60, Class=class_item)
        slot3 = Slot.create(SlotUid=uuid.uuid4(), DayOfWeek=5, StartTime=time(18, 0), Duration=60, Class=class_item)
        # Sessions
        teacher = date.today()
        t1 = teacher + timedelta(days=7)
        session1 = Session.create(StartDateTime=datetime.combine(teacher, slot1.StartTime), Duration=slot1.Duration, Slot=slot1, Class=class_item)
        session2 = Session.create(StartDateTime=datetime.combine(teacher, slot2.StartTime), Duration=slot2.Duration, Slot=slot2, Class=class_item)
        session3 = Session.create(StartDateTime=datetime.combine(teacher, slot3.StartTime), Duration=slot3.Duration, Slot=slot3, Class=class_item)
        session4 = Session.create(StartDateTime=datetime.combine(t1, slot1.StartTime), Duration=slot1.Duration, Slot=slot1, Class=class_item)
        session5 = Session.create(StartDateTime=datetime.combine(t1, slot2.StartTime), Duration=slot2.Duration, Slot=slot2, Class=class_item)
        session6 = Session.create(StartDateTime=datetime.combine(t1, slot3.StartTime), Duration=slot3.Duration, Slot=slot3, Class=class_item)

        start = session1.StartDateTime
        end = session6.StartDateTime + timedelta(minutes=session6.Duration)
    print(f'id = {user_data.id}')

    # Enrollment:
    with db.atomic():
        enroll_class = Class.get(Class.Name == 'Music')
        enroll_student1 = UserData.get(UserData.Login == 'student1@goncharov.dev')
        enroll_student2 = UserData.get(UserData.Login == 'student2@goncharov.dev')

        student1_enrollment = Enrollment.create(StartDate=start, EndDate=end, Notes='', Student=enroll_student1.Student, Class=enroll_class)
        student1_enrollment.save()
        student2_enrollment = Enrollment.create(StartDate=start, EndDate=end, Notes='', Student=enroll_student2.Student, Class=enroll_class)
        student2_enrollment.save()

    # CheckIns:
    with db.atomic():
        enroll_class = Class.get(Class.Name == 'Music')
        enroll_student1 = UserData.get(UserData.Login == 'student1@goncharov.dev')
        enroll_student2 = UserData.get(UserData.Login == 'student2@goncharov.dev')
        session_1 = Session.select().where(Session.Class == enroll_class).order_by(Session.StartDateTime)[1]
        check_in0 = CheckIn.create(CheckInStatus=CheckInStatus.Present, TimeStamp=datetime.now(), Student=enroll_student1.Student, Session=session_1)
        check_in0.save()
        check_in1 = CheckIn.create(CheckInStatus=CheckInStatus.Absent, TimeStamp=datetime.now(), Student=enroll_student2.Student, Session=session_1)
        check_in1.save()

        session_last = Session.select().where(Session.Class == enroll_class).order_by(Session.StartDateTime)[-1]
        check_in2 = CheckIn.create(CheckInStatus=CheckInStatus.Present, TimeStamp=datetime.now(), Student=enroll_student1.Student, Session=session_last)
        check_in2.save()
        check_in3 = CheckIn.create(CheckInStatus=CheckInStatus.Absent, TimeStamp=datetime.now(), Student=enroll_student2.Student, Session=session_last)
        check_in3.save()

    # Output
    with db:
        non_existing = Teacher.get_or_none(Teacher.FirstName == 'ig')
        assert non_existing is None

        teacher = Teacher[1]
        #teacher1 = Teacher[2]
        assert teacher.Students.count()
        for associated_student in teacher.Students.where(TutorStudentAssociation.Status == AssociationStatus.Active):
            student = associated_student.Student
            print(f'{student.id} {associated_student.Status} {student.FirstName}')

        enrolled_student1 = UserData.get(UserData.Login == 'student1@goncharov.dev').Student
        enrolled_student2 = UserData.get(UserData.Login == 'student2@goncharov.dev').Student

        check_session_1 = Session.select().where(Session.Class == enroll_class).order_by(Session.StartDateTime)[1]
        check_session_last = Session.select().where(Session.Class == enroll_class).order_by(Session.StartDateTime)[-1]

        for location in teacher.Locations:
            print(f'{location.id} - {location.Url}')

        class_item = Class.get(Class.Name == 'Music')
        slots = class_item.Slots
        print(f'Count(Slots) = {slots.count()}')
        assert slots.count() == 3
        for slot in slots:
            print(f'{slot.SlotUid} - {slot.StartTime}')

        sessions = class_item.Sessions
        print(f'Count(Session) = {sessions.count()}')
        assert sessions.count() == 6

        enrollments = class_item.Enrollments
        print(f'Count(Enrollment) = {enrollments.count()}')

        all_checkins = CheckIn.select().count()
        print(f'All Count(CheckIn) = {all_checkins}')
        assert all_checkins == 4

        present_count = CheckIn.select().join(Session).where(CheckIn.Session.Class == class_item) \
            .where(CheckIn.Student == enrolled_student1).where(CheckIn.CheckInStatus == CheckInStatus.Present).count()
        print(f'{class_item.Name} Count(CheckIn)==Present - {present_count}')
        assert present_count == 2

        present_count_session1 = CheckIn.select().where(CheckIn.Session == check_session_1) \
            .where(CheckIn.Student == enrolled_student1).where(CheckIn.CheckInStatus == CheckInStatus.Present).count()
        print(f'{class_item.Name} at {check_session_1.StartDateTime}+{check_session_1.Duration}m Count(CheckIn)==Present - {present_count_session1}')
        assert present_count_session1 == 1

        absent_count = CheckIn.select().join(Session).where(CheckIn.Session.Class == class_item) \
            .where(CheckIn.Student == enrolled_student2).where(CheckIn.CheckInStatus == CheckInStatus.Absent).count()
        print(f'{class_item.Name} Count(CheckIn)==Absent - {absent_count}')
        assert absent_count == 2

        absent_count_last_session = CheckIn.select().where(CheckIn.Session == check_session_last) \
            .where(CheckIn.Student == enrolled_student1).where(CheckIn.CheckInStatus == CheckInStatus.Present).count()
        print(f'{class_item.Name} at {check_session_last.StartDateTime}+{check_session_1.Duration}m Count(CheckIn)==Present - {absent_count_last_session}')
        assert absent_count_last_session == 1


if __name__ == '__main__':
    main()
