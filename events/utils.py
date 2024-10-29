from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from events.models import Event


def handle_event_registration(event: Event, user: User, register: bool) -> str:
    """Handles user registration or un-registration for an event.

    Validates that the event is in the future, and that the user is not the owner of the event.
    Checks the event capacity.
    Registers or unregisters the user based on the provided flag.

    Args:
        event (Event): The event to register/unregister for.
        user (User): The user attempting to register/unregister.
        register (bool): Indicates if the user should be registered (`True`) or unregistered (`False`).

    Returns:
        str: Success message indicating the action taken.

    Raises:
        ValidationError: If any validation step fails.
    """
    if event.start_date < timezone.now().date():
        raise ValidationError("Cannot modify registration for past events.")

    if user == event.owner:
        raise ValidationError("The owner of the event cannot register or unregister.")

    if register:
        if user in event.attendees.all():
            raise ValidationError("User is already registered for this event.")

        # Checking the events maximum capacity
        if event.capacity is not None and event.attendees.count() >= event.capacity:
            raise ValidationError("Event has reached maximum capacity.")

        event.attendees.add(user)
        return "Registered successfully."
    else:
        if user not in event.attendees.all():
            raise ValidationError("User is not registered for this event.")
        event.attendees.remove(user)
        return "Unregistered successfully."
