from datetime import datetime

from django_filters import rest_framework as filters

from .models import Schedule


class ScheduleFilter(filters.FilterSet):
    for_today = filters.BooleanFilter(method="filter_today")
    class_name = filters.CharFilter(field_name="class_group__name")

    class Meta:
        model = Schedule
        fields = ["for_today", "class_name"]

    def get_current_day(self):
        return datetime.now().isoweekday()

    def filter_today(self, queryset, name, value):
        if value:
            current_day = self.get_current_day()
            return queryset.filter(day_of_week=min(current_day, 5))

        return queryset
