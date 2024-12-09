from django.test import TestCase
from datetime import datetime
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Class, Student, Teacher, Subject, Schedule


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_data(db):
    # Create test data
    class_5a = Class.objects.create(name='5A')
    student = Student.objects.create(name='John Doe')
    class_5a.students.add(student)
    
    teacher = Teacher.objects.create(name='Alex')
    subject = Subject.objects.create(name='Math', teacher=teacher)
    
    schedule = Schedule.objects.create(
        class_group=class_5a,
        subject=subject,
        day_of_week=1,  # Monday
        hour=1
    )
    return {'schedule': schedule, 'class': class_5a}


@pytest.mark.django_db
def test_list_schedules(api_client, sample_data):
    url = reverse('schedule-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['class_group']['name'] == '5A'
    assert response.data['results'][0]['subject']['name'] == 'Math'
    assert response.data['results'][0]['teacher']['name'] == 'Alex'


@pytest.mark.django_db
def test_filter_schedule_by_class(api_client, sample_data):
    url = reverse('schedule-list')
    response = api_client.get(url, {'class_name': '5A'})
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['class_group']['name'] == '5A'


@pytest.mark.django_db
def test_filter_schedule_for_today(api_client, sample_data):
    url = reverse('schedule-list')
    response = api_client.get(url, {'for_today': 'true'})
    
    assert response.status_code == status.HTTP_200_OK
    current_day = datetime.now().isoweekday()
    
    if current_day <= 5:  # Weekday
        assert len(response.data['results']) == (1 if current_day == 1 else 0)
    else:  # Weekend
        assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_filter_schedule_for_today_and_class(api_client, sample_data):
    url = reverse('schedule-list')
    response = api_client.get(url, {'for_today': 'true', 'class_name': '5A'})
    
    assert response.status_code == status.HTTP_200_OK
    current_day = datetime.now().isoweekday()
    
    if current_day <= 5:  # Weekday
        assert len(response.data['results']) == (1 if current_day == 1 else 0)
    else:  # Weekend
        assert len(response.data['results']) == 0
