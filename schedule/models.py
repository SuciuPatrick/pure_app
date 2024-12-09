from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()

    class Meta:
        verbose_name_plural = 'classes'


class Student(models.Model):
    name = models.CharField(max_length=100)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
    ]

    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, validators=[MinValueValidator(1), MaxValueValidator(5)])
    hour = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])

    class Meta:
        ordering = ['day_of_week', 'hour']
        unique_together = [
            ['class_group', 'day_of_week', 'hour'],  # Prevent multiple lessons at the same time for a class
            ['subject', 'day_of_week', 'hour'],      # Prevent teacher from teaching multiple classes at the same time
        ]

    def __str__(self):
        return f"{self.class_group} - {self.subject} ({self.get_day_of_week_display()}, hour {self.hour})"
