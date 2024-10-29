from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_events"
    )
    attendees = models.ManyToManyField(
        User, related_name="attending_events", blank=True
    )
    capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
