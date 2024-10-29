import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.integration.utils.auth_utils import get_auth_headers

User = get_user_model()
pytest_plugins = ["tests.integration.utils.fixtures"]


@pytest.mark.django_db
def test_list_events(api_client, user, event):
    response = api_client.get(reverse("event-list"), headers=get_auth_headers(user))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == event.name


@pytest.mark.django_db
def test_list_owned_events(api_client, user, event, user2):
    response = api_client.get(
        reverse("event-list") + f"?owner={user.id}", headers=get_auth_headers(user)
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == event.name


@pytest.mark.django_db
def test_list_owned_events_filter_by_start_date(
    api_client, user, event, user2, event_2, fixed_datetime
):
    response = api_client.get(
        reverse("event-list") + f"?start_date=2024-01-03",
        headers=get_auth_headers(user),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == event_2.name
    response = api_client.get(
        reverse("event-list") + f"?start_date=2023-01-03",
        headers=get_auth_headers(user),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_list_owned_events_filter_by_status(
    api_client, user, event, user2, event_2, fixed_datetime
):
    response = api_client.get(
        reverse("event-list") + f"?status=future", headers=get_auth_headers(user)
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_event(api_client, user):
    data = {
        "name": "new event",
        "description": "description",
        "start_date": "2024-02-01",
        "end_date": "2024-02-02",
        "capacity": 5,
    }
    response = api_client.post(
        reverse("event-list"), headers=get_auth_headers(user), data=data
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert response.data["owner"] == user.id


@pytest.mark.django_db
def test_update_event_owner(api_client, user, event):
    data = {"name": "updated event", "description": "new description"}
    response = api_client.patch(
        reverse("event-detail", args=[event.id]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_update_event_non_owner(api_client, user2, event):
    data = {"name": "name"}
    response = api_client.put(reverse("event-detail", args=[event.id]), data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_event_owner(api_client, user, event):
    response = api_client.delete(
        reverse("event-detail", args=[event.id]), headers=get_auth_headers(user)
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_event_non_owner(api_client, user2, event):
    response = api_client.delete(reverse("event-detail", args=[event.id]))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_register_for_event(api_client, user, event_2, fixed_datetime):
    data = {"register": True}
    response = api_client.post(
        reverse("event-register", args=[event_2.id]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data


@pytest.mark.django_db
def test_register_for_event_over_capacity(
    api_client, user, user3, event_2, fixed_datetime
):
    event_2.attendees.add(user)
    data = {"register": True}
    response = api_client.post(
        reverse("event-register", args=[event_2.id]),
        headers=get_auth_headers(user3),
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unregister_from_event(api_client, user, event_2, fixed_datetime):
    event_2.attendees.add(user)
    data = {"register": False}
    response = api_client.post(
        reverse("event-register", args=[event_2.id]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_register_event_not_found(api_client, user):
    data = {"register": True}
    response = api_client.post(
        reverse("event-register", args=[9999]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_register_invalid_data(api_client, user, event):
    data = {"register": "not_a_boolean"}
    response = api_client.post(
        reverse("event-register", args=[event.id]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_for_past_event(api_client, user, event, user2):
    data = {"register": True}
    response = api_client.post(
        reverse("event-register", args=[event.id]),
        headers=get_auth_headers(user2),
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_owner_of_an_event(api_client, user, event):
    data = {"register": True}
    response = api_client.post(
        reverse("event-register", args=[event.id]),
        headers=get_auth_headers(user),
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
