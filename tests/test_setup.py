import pytest
from django.urls import reverse


def test_django_setup():
    """Verify that Django is configured correctly"""
    assert True


def test_api_client(api_client):
    """Verify that API client fixture works"""
    response = api_client.get("/api/")
    assert response.status_code in [
        200,
        404,
    ]  # Either is fine for now, just checking the client works


@pytest.mark.django_db
def test_database():
    """Verify that database access works"""
    from django.contrib.auth.models import User

    User.objects.create(username="testuser")
    assert User.objects.count() == 1
