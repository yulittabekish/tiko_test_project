from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event
from events.permissions import IsEventOwner
from events.serializers import (EventRegistrationSerializer, EventSerializer,
                                ReadEventSerializer)
from events.utils import handle_event_registration
from tokens_auth.permissions import HasValidAccessToken


class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD actions for events.
    Users can create, update, and view events, with restrictions based on ownership.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [HasValidAccessToken, IsEventOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadEventSerializer
        return EventSerializer

    @extend_schema(
        request=EventRegistrationSerializer
    )
    @action(
        detail=True,
        methods=["post"],
        serializer_class=EventRegistrationSerializer,
        permission_classes=[HasValidAccessToken],
    )
    def register(self, request, pk=None):
        """
        Custom action to register or unregister a user for an event based on a flag in the request.

        Args:
            request (Request): The request object containing user data.
            pk (int): The primary key of the event.

        Returns:
            Response: Success or error message based on the action.
        """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            message = handle_event_registration(
                event=event,
                user=request.user,
                register=serializer.validated_data["register"],
            )
            return Response({"message": message}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
