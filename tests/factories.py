import factory
from factory.django import DjangoModelFactory
from api.models import Teacher, Subject, Class, Schedule, Student


class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    name = factory.Faker('name')


class ClassFactory(DjangoModelFactory):
    class Meta:
        model = Class

    name = factory.Sequence(lambda n: f'Class {n}')
    # student_count = factory.LazyAttribute(lambda obj: obj.students.count())


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    name = factory.Faker('name')
    class_group = factory.SubFactory(ClassFactory)


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Sequence(lambda n: f'Subject {n}')
    teacher = factory.SubFactory(TeacherFactory)


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = Schedule

    class_group = factory.SubFactory(ClassFactory)
    subject = factory.SubFactory(SubjectFactory)
    day_of_week = factory.Faker('random_int', min=1, max=5)
    hour = factory.Faker('random_int', min=1, max=8)
