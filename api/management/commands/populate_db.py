import random

from django.core.management.base import BaseCommand
from faker import Faker

from api.models import (
    Class,
    Schedule,
    Student,
    Subject,
    Teacher,
)

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def create_classes(self, class_names):
        """Create classes"""
        classes = []
        for name in class_names:
            class_obj = Class.objects.create(name=name)
            classes.append(class_obj)
        return classes

    def create_students(self, classes, total_students=200):
        """Create students and assign them to classes"""
        students = []
        # Distribute students evenly among classes
        students_per_class = total_students // len(classes)

        for class_obj in classes:
            for _ in range(students_per_class):
                student = Student.objects.create(
                    name=fake.name(), class_group=class_obj
                )
                students.append(student)
        return students

    def create_teachers(self, count=15):
        """Create teachers with titles and fake names"""
        teachers = []
        teacher_titles = ["Mr.", "Ms.", "Mrs.", "Dr."]
        for _ in range(count):
            title = random.choice(teacher_titles)
            name = f"{title} {fake.last_name()}"
            teacher = Teacher.objects.create(name=name)
            teachers.append(teacher)
        return teachers

    def create_subjects(self, subject_names, teachers):
        """Create subjects and assign teachers"""
        subjects = []
        for subject_name in subject_names:
            # Create 1 or 2 teachers per subject
            for _ in range(random.randint(1, 2)):
                subject = Subject.objects.create(
                    name=subject_name, teacher=random.choice(teachers)
                )
                subjects.append(subject)
        return subjects

    def create_schedules(self, classes, subjects):
        """Create weekly schedules for all classes"""
        schedules_created = 0

        for class_obj in classes:
            for day in range(1, 6):  # Monday to Friday
                for hour in range(1, 8):  # 7 hours per day
                    Schedule.objects.create(
                        class_group=class_obj,
                        subject=random.choice(subjects),
                        day_of_week=day,
                        hour=hour,
                    )
                    schedules_created += 1

        return schedules_created

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample data...")

        # Configuration
        class_names = ["5A", "5B", "5C", "5D", "6A", "6B", "6C", "6D"]
        subject_names = [
            "Mathematics",
            "English Literature",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Art",
            "Music",
            "Physical Education",
        ]

        # Create all data
        classes = self.create_classes(class_names)
        self.stdout.write(self.style.SUCCESS(f"Created {len(classes)} classes"))

        students = self.create_students(classes)
        self.stdout.write(self.style.SUCCESS(f"Created {len(students)} students"))

        teachers = self.create_teachers()
        self.stdout.write(self.style.SUCCESS(f"Created {len(teachers)} teachers"))

        subjects = self.create_subjects(subject_names, teachers)
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(subjects)} subject-teacher combinations")
        )

        schedules = self.create_schedules(classes, subjects)
        self.stdout.write(self.style.SUCCESS(f"Created {schedules} schedule entries"))

        # Print statistics
        self.stdout.write("\nDatabase Statistics:")
        self.stdout.write(
            f"Average class size: {Student.objects.count() / Class.objects.count():.1f} students"
        )
        self.stdout.write(
            f"Subjects per teacher: {Subject.objects.count() / Teacher.objects.count():.1f}"
        )

        self.stdout.write(self.style.SUCCESS("\nDatabase populated successfully!"))
