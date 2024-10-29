from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


class IsEventOwner(BasePermission):
    """
    Custom permission to allow only event owners to edit or delete their events.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if not obj.owner == request.user:
            raise AuthenticationFailed("Can't update or delete events of other owners.")
        else:
            return True
