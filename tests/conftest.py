import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    yield APIClient()
