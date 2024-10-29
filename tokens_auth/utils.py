from enum import Enum
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_user_password(password: str, user: User) -> None:
    """Validate password constraints for a user.

    Args:
        password (str): 'password' value.
        user (User): User instance.

    Raises:
        serializers.ValidationError: If password validation fails.
    """
    try:
        validate_password(password, user)
    except ValidationError as e:
        raise serializers.ValidationError({"password": e.messages})
