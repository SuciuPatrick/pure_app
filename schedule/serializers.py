from rest_framework import serializers
from .models import Class, Subject, Teacher, Schedule


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ['name', 'student_count']


class ScheduleSerializer(serializers.ModelSerializer):
    class_group = ClassSerializer()
    subject = SubjectSerializer()
    teacher = TeacherSerializer(source='subject.teacher')
    day_of_week = serializers.CharField(source='get_day_of_week_display')

    class Meta:
        model = Schedule
        fields = ['class_group', 'subject', 'day_of_week', 'hour', 'teacher'] 