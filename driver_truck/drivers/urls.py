from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'drivers', DriverViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]