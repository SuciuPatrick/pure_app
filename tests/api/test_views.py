import logging
from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

from api.filters import ScheduleFilter
from tests.factories import (
    ClassFactory,
    ScheduleFactory,
)


@pytest.mark.django_db
class TestScheduleViewSet:
    """Test basic CRUD operations for ScheduleViewSet"""

    def test_list_schedules(self, api_client):
        # Create some test schedules
        ScheduleFactory.create_batch(3)

        url = reverse("schedule-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3


@pytest.mark.django_db
class TestScheduleFilters:
    """Test filtering functionality for ScheduleViewSet"""

    def test_filter_by_class_name(self, api_client):
        # Create a class and its schedules
        class_group = ClassFactory(name="9A")
        ScheduleFactory.create_batch(2, class_group=class_group)
        ScheduleFactory()  # Different class

        url = reverse("schedule-list")
        response = api_client.get(url, {"class_name": "9A"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert all(
            item["class_group"]["name"] == "9A" for item in response.data["results"]
        )

    @mock.patch.object(ScheduleFilter, "get_current_day")
    def test_filter_for_today_weekday(self, mock_get_current_day, api_client):
        # Mock to return Wednesday (3)
        mock_get_current_day.return_value = 3

        # Create schedules for different days
        ScheduleFactory.create_batch(2, day_of_week=3)  # Wednesday
        ScheduleFactory(day_of_week=2)  # Tuesday

        url = reverse("schedule-list")
        response = api_client.get(url, {"for_today": "true"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert all(
            item["day_of_week"] == "Wednesday" for item in response.data["results"]
        )

    @mock.patch.object(ScheduleFilter, "get_current_day")
    def test_filter_for_today_weekend(self, mock_get_current_day, api_client):
        # Mock to return Sunday (7)
        mock_get_current_day.return_value = 7

        # Create schedules for Friday and Monday
        ScheduleFactory.create_batch(2, day_of_week=5)  # Friday
        ScheduleFactory(day_of_week=1)  # Monday

        url = reverse("schedule-list")
        response = api_client.get(url, {"for_today": "true"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

        assert all(item["day_of_week"] == "Friday" for item in response.data["results"])


@pytest.mark.django_db
class TestScheduleCache:
    """Test caching functionality for ScheduleViewSet"""

    def test_cache_hit(self, api_client):
        from django.core.cache import cache

        ScheduleFactory.create_batch(3)
        url = reverse("schedule-list")
        cache_key = f"schedule:view:{url}"

        # First request - should be a cache miss
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK

        # Verify data was cached
        cached_data = cache.get(cache_key)
        assert cached_data == response1.data

        # Second request - should hit cache
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data == response1.data

    def test_cache_invalidation_on_create(self, api_client):
        from django.core.cache import cache

        url = reverse("schedule-list")
        cache_key = f"schedule:view:{url}"

        # Initial request
        response1 = api_client.get(url)
        initial_data = response1.data

        # Verify data is in cache
        assert cache.get(cache_key) == initial_data

        # Create new schedule (should trigger invalidation)
        ScheduleFactory()

        # Verify cache was invalidated
        assert cache.get(cache_key) is None

        # Next request should get fresh data
        response2 = api_client.get(url)
        assert response2.data != initial_data
