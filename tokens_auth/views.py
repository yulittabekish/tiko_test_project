from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView

from tokens_auth.serializers import LoginSerializer, RefreshTokenSerializer, RegisterSerializer
from tokens_auth.services import TokenService

service = TokenService()


class RegisterView(GenericAPIView):
    """API view for user registration."""

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if user:
            tokens = service.generate_token_pair(user.id)
            return JsonResponse(tokens, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """API view for user login."""

    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user:
            tokens = service.generate_token_pair(user.id)
            return JsonResponse(tokens)


class RefreshTokenView(GenericAPIView):
    """API view for refreshing token pair."""

    serializer_class = RefreshTokenSerializer

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        payload = service.validate_refresh_token(refresh_token)

        if payload:
            new_tokens = service.generate_token_pair(payload["user_id"])
            return JsonResponse(new_tokens)
        return JsonResponse({"error": "Invalid or expired refresh token"}, status=400)
