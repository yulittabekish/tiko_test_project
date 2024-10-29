import datetime

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.integration.utils.auth_utils import get_auth_headers

from tokens_auth.services import TokenService, TokenType

pytest_plugins = ["tests.integration.utils.fixtures"]


@pytest.mark.django_db
def test_register(api_client):
    data = {"email": "test@gmail.com", "username": "username", "password": "test1234!"}
    response = api_client.post(reverse("register"), data=data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_register_invalid_password(api_client):
    data = {"email": "test@gmail.com", "username": "username", "password": "test"}
    response = api_client.post(reverse("register"), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    User = get_user_model()
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_register_bad_request(api_client):
    data = {"email": "test@gmail.com", "password": "test1234!"}
    response = api_client.post(reverse("register"), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login(api_client, user):
    data = {"username": user.username, "password": user.password}
    response = api_client.post(reverse("login"), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] and response.json()["refresh_token"]


@pytest.mark.django_db
def test_login_fail(api_client):
    data = {"email": "test@gmail.com", "password": "password"}
    response = api_client.post(reverse("login"), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_refresh_token(api_client, user):
    refresh_token = TokenService().create_token(
        user.id,
        token_type=TokenType.REFRESH,
        lifetime=datetime.timedelta(hours=int(settings.REFRESH_TOKEN_LIFETIME)),
    )
    data = {"refresh_token": refresh_token}

    response = api_client.post(reverse("refresh"), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] and response.json()["refresh_token"]


@pytest.mark.django_db
def test_refresh_token(api_client):
    data = {"refresh_token": "invalid_token"}

    response = api_client.post(reverse("refresh"), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
