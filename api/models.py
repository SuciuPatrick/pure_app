from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import signals
from django.dispatch import receiver
from api.cache import invalidate_schedule_cache


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)
    student_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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


# Student count signals
@receiver(signals.post_save, sender=Student)
def update_class_student_count_on_save(sender, instance, **kwargs):
    if instance.class_group:
        instance.class_group.student_count = instance.class_group.students.count()
        instance.class_group.save(update_fields=['student_count'])


@receiver(signals.post_delete, sender=Student)
def update_class_student_count_on_delete(sender, instance, **kwargs):
    if instance.class_group:
        instance.class_group.student_count = instance.class_group.students.count()
        instance.class_group.save(update_fields=['student_count'])


@receiver(signals.pre_save, sender=Student)
def update_old_class_student_count(sender, instance, **kwargs):
    if instance.pk:  # Only for existing students
        try:
            old_student = Student.objects.get(pk=instance.pk)
            if old_student.class_group and old_student.class_group != instance.class_group:
                # Update the old class count
                old_student.class_group.student_count = old_student.class_group.students.count() - 1
                old_student.class_group.save(update_fields=['student_count'])
        except Student.DoesNotExist:
            pass


# Cache invalidation signals
@receiver([signals.post_save, signals.post_delete], sender=Schedule)
@receiver([signals.post_save, signals.post_delete], sender=Subject)
@receiver([signals.post_save, signals.post_delete], sender=Teacher)
@receiver([signals.post_save, signals.post_delete], sender=Class)
def invalidate_cache_on_change(sender, **kwargs):
    """Invalidate cache when any related model changes"""
    invalidate_schedule_cache()
