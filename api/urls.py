from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from .views import ScheduleViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register("schedule", ScheduleViewSet, basename="schedule")

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
