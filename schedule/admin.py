from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Student, Class, Teacher, Subject, Schedule


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_count']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_group']
    list_filter = ['class_group']
    search_fields = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher']
    list_filter = ['teacher']
    search_fields = ['name', 'teacher__name']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['class_group', 'subject', 'teacher_link', 'day_of_week', 'hour']
    list_filter = ['class_group', 'subject', 'subject__teacher', 'day_of_week']
    search_fields = ['class_group__name', 'subject__name', 'subject__teacher__name']
    ordering = ['day_of_week', 'hour']

    def teacher_link(self, obj):
        url = reverse('admin:schedule_teacher_change', args=[obj.subject.teacher.id])
        return format_html('<a href="{}">{}</a>', url, obj.subject.teacher.name)
    teacher_link.short_description = 'Teacher'
    teacher_link.admin_order_field = 'subject__teacher__name'
