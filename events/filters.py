from django.db import models
from django_filters import rest_framework
from django.utils import timezone
from events.models import Event

class EventStatus(models.TextChoices):
    PAST = "past", "Past Events"
    FUTURE = "future", "Future Events"

class EventFilter(rest_framework.FilterSet):
    owner = rest_framework.NumberFilter(field_name="owner__id", lookup_expr="exact")
    start_date = rest_framework.DateFilter(field_name="start_date", lookup_expr="exact")
    end_date = rest_framework.DateFilter(field_name="end_date", lookup_expr="exact")

    status = rest_framework.ChoiceFilter(
        method="filter_by_status",
        choices=EventStatus.choices,
    )

    class Meta:
        model = Event
        fields = ["start_date", "end_date", "status", "owner"]

    def filter_by_status(self, queryset, name, value):
        today = timezone.now().date()
        if value == EventStatus.PAST:
            return queryset.filter(end_date__lt=today)
        elif value == EventStatus.FUTURE:
            filtered_queryset = queryset.filter(start_date__gt=today)
            return filtered_queryset
        return queryset
