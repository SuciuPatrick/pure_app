from datetime import datetime
from django.db.models import Prefetch
from rest_framework import viewsets, mixins
from rest_framework.filters import BaseFilterBackend
from .models import Schedule, Subject
from .serializers import ScheduleSerializer
from .utils import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ScheduleFilter
from .cache import cache_schedule_view


class ScheduleViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Schedule.objects.select_related(
            'class_group',
            'subject',
            'subject__teacher'
        ).order_by('day_of_week', 'hour')

    @cache_schedule_view(timeout=60 * 15)  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
