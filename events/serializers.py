from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.models import Event


class ReadEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("owner", "attendees")

    def validate(self, attrs: dict) -> dict:
        """Validate that the event's end date is not before the start date.

        Args:
            attrs (dict): The attributes to validate.

        Returns:
            dict: Validated attributes.

        Raises:
            ValidationError: If `end_date` is earlier than `start_date`.
        """
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        return attrs

    def create(self, validated_data: dict) -> Event:
        """Create a new Event instance with the current user as the owner.

        Args:
            validated_data (dict): Validated data for creating an event.

        Returns:
            Event: New Event instance.
        """
        request = self.context.get("request")
        owner = None
        if request and hasattr(request, "user"):
            User = get_user_model()
            owner = User.objects.get(id=request.user.id)
        event = Event.objects.create(**validated_data, owner=owner)
        return event


class EventRegistrationSerializer(serializers.Serializer):
    register = serializers.BooleanField()
