# Generated by Django 4.2.17 on 2024-12-09 15:27

from django.db import migrations, models


def initialize_student_count(apps, schema_editor):
    Class = apps.get_model('schedule', 'Class')
    for class_instance in Class.objects.all():
        class_instance.student_count = class_instance.students.count()
        class_instance.save(update_fields=['student_count'])


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_remove_class_students_student_class_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='student_count',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(initialize_student_count),
    ]