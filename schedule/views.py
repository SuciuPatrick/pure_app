from datetime import datetime
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend
from .models import Schedule, Subject
from .serializers import ScheduleSerializer
from .utils import StandardResultsSetPagination


class TodayClassFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        for_today = request.query_params.get('for_today', '').lower() == 'true'
        class_name = request.query_params.get('class_name')

        if for_today:
            # Get current day of week (1-7, where 1 is Monday)
            current_day = datetime.now().isoweekday()
            queryset = queryset.filter(day_of_week=min(current_day, 5))  # Only show weekdays

        if class_name:
            queryset = queryset.filter(class_group__name=class_name)

        return queryset


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScheduleSerializer
    filter_backends = [TodayClassFilterBackend]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Schedule.objects.select_related(
            'class_group',
            'subject',
            'subject__teacher'
        ).order_by('day_of_week', 'hour')
