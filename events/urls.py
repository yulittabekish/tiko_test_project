from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

router = DefaultRouter()
router.register("", EventViewSet, basename="event")
urlpatterns = [
    path("", include(router.urls)),
]
