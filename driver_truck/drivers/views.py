from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .models import Driver, Vehicle
from .serializers import (
    DriverSerializer, DriverListSerializer,
    VehicleSerializer, VehicleListSerializer
)


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Driver model
    """
    queryset = Driver.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for driver creation
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DriverListSerializer
        return DriverSerializer
    
    def get_queryset(self):
        queryset = Driver.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by carrier
        carrier = self.request.query_params.get('carrier')
        if carrier:
            queryset = queryset.filter(carrier_name__icontains=carrier)
        
        return queryset.order_by('username')
    
    @action(detail=True, methods=['get'])
    def duty_logs(self, request, pk=None):
        """
        Get duty logs for a specific driver
        """
        driver = self.get_object()
        logs = driver.duty_logs.all()[:10]  # Last 10 logs
        
        from logs.serializers import DutyLogListSerializer
        serializer = DutyLogListSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def trips(self, request, pk=None):
        """
        Get trips for a specific driver
        """
        driver = self.get_object()
        trips = driver.trips.all()[:10]  # Last 10 trips
        
        from trips.serializers import TripListSerializer
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def current_status(self, request, pk=None):
        """
        Get current duty status for a driver
        """
        driver = self.get_object()
        current_log = driver.duty_logs.filter(end_time__isnull=True).first()
        
        if current_log:
            from logs.serializers import DutyLogSerializer
            serializer = DutyLogSerializer(current_log)
            return Response(serializer.data)
        
        return Response({'status': 'No active duty log'}, status=status.HTTP_404_NOT_FOUND)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vehicle model
    """
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VehicleListSerializer
        return VehicleSerializer
    
    def get_queryset(self):
        queryset = Vehicle.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by assigned driver
        driver_id = self.request.query_params.get('driver')
        if driver_id:
            queryset = queryset.filter(assigned_driver_id=driver_id)
        
        # Filter by make
        make = self.request.query_params.get('make')
        if make:
            queryset = queryset.filter(make__icontains=make)
        
        return queryset.order_by('license_plate')
    
    @action(detail=True, methods=['post'])
    def assign_driver(self, request, pk=None):
        """
        Assign a driver to a vehicle
        """
        vehicle = self.get_object()
        driver_id = request.data.get('driver_id')
        
        if not driver_id:
            return Response(
                {'error': 'driver_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            driver = Driver.objects.get(id=driver_id)
            vehicle.assigned_driver = driver
            vehicle.save()
            
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        
        except Driver.DoesNotExist:
            return Response(
                {'error': 'Driver not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def unassign_driver(self, request, pk=None):
        """
        Unassign driver from a vehicle
        """
        vehicle = self.get_object()
        vehicle.assigned_driver = None
        vehicle.save()
        
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
