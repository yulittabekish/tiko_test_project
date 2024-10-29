from datetime import datetime

import pytest
import pytz
from django.contrib.auth import get_user_model

from events.models import Event

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="user1", password="testpass")


@pytest.fixture
def user2():
    return User.objects.create_user(username="user2", password="testpass")


@pytest.fixture
def user3():
    return User.objects.create_user(username="user3", password="testpass")


@pytest.fixture
def event(user):
    return Event.objects.create(
        name="event1",
        description="description",
        start_date="2023-01-01",
        end_date="2023-01-02",
        owner=user,
        capacity=100,
    )


@pytest.fixture
def event_2(user2):
    return Event.objects.create(
        name="event2",
        description="description",
        start_date="2024-01-03",
        end_date="2024-01-04",
        owner=user2,
        capacity=1,
    )


@pytest.fixture(scope="function")
def fixed_datetime(monkeypatch) -> datetime:
    fixed_datetime = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
    monkeypatch.setattr("django.utils.timezone.now", lambda: fixed_datetime)
    return fixed_datetime
