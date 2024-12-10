from django.core.management.base import BaseCommand
from api.models import Student, Class, Teacher, Subject, Schedule


class Command(BaseCommand):
    help = 'Cleans all tables from the schedule app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning database...')

        # Delete in order to respect foreign key constraints
        self.stdout.write('Deleting schedules...')
        Schedule.objects.all().delete()
        
        self.stdout.write('Deleting subjects...')
        Subject.objects.all().delete()
        
        self.stdout.write('Deleting students...')
        Student.objects.all().delete()
        
        self.stdout.write('Deleting teachers...')
        Teacher.objects.all().delete()
        
        self.stdout.write('Deleting classes...')
        Class.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned all tables!')) 