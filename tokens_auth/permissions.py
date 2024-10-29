from django.contrib.auth import get_user_model
from rest_framework import permissions

from tokens_auth.services import TokenService
from rest_framework.exceptions import AuthenticationFailed


class HasValidAccessToken(permissions.BasePermission):
    """
    Custom permission to check for a valid access token.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ")[1]
            payload = TokenService().validate_access_token(token)
            User = get_user_model()
            if payload:
                try:
                    request.user = User.objects.get(pk=payload["user_id"])
                    return True
                except User.DoesNotExist:
                    raise AuthenticationFailed("Invalid token user.")

        raise AuthenticationFailed("Invalid or missing access token.")
