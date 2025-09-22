from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, TripStopViewSet, TripEventViewSet

router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'stops', TripStopViewSet)
router.register(r'events', TripEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]