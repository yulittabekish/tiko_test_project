from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)
        write_only_fields = ("password",)

    def validate(self, attrs):
        User = get_user_model()
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        user = User.objects.create_user(**attrs)
        if password := attrs.get("password"):
            validate_password(password, user)
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        User = get_user_model()
        user = User.objects.get(username=attrs["username"])
        if password := attrs.get("password"):
            validate_password(password, user)
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
