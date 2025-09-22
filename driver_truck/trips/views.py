from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from .models import Trip, TripStop, TripEvent
from .serializers import (
    TripSerializer, TripCreateSerializer, TripListSerializer,
    TripStopSerializer, TripStopCreateSerializer,
    TripEventSerializer, TripEventCreateSerializer
)


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip model
    """
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TripCreateSerializer
        elif self.action == 'list':
            return TripListSerializer
        return TripSerializer
    
    def get_queryset(self):
        queryset = Trip.objects.all()
        
        # Filter by driver
        driver_id = self.request.query_params.get('driver')
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(planned_start_time__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(planned_start_time__date__lte=end_date)
            except ValueError:
                pass
        
        return queryset.order_by('-planned_start_time')
    
    @action(detail=True, methods=['post'])
    def start_trip(self, request, pk=None):
        """
        Start a trip
        """
        trip = self.get_object()
        
        if trip.status != 'planned':
            return Response(
                {'error': 'Trip can only be started from planned status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.status = 'in_progress'
        trip.actual_start_time = timezone.now()
        trip.save()
        
        # Create start event
        TripEvent.objects.create(
            trip=trip,
            event_type='start',
            event_time=trip.actual_start_time,
            description='Trip started'
        )
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete_trip(self, request, pk=None):
        """
        Complete a trip
        """
        trip = self.get_object()
        
        if trip.status != 'in_progress':
            return Response(
                {'error': 'Trip can only be completed from in_progress status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        actual_distance = request.data.get('actual_distance')
        
        trip.status = 'completed'
        trip.actual_end_time = timezone.now()
        if actual_distance:
            trip.actual_distance = actual_distance
        trip.save()
        
        # Create completion event
        TripEvent.objects.create(
            trip=trip,
            event_type='complete',
            event_time=trip.actual_end_time,
            description='Trip completed'
        )
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stops(self, request, pk=None):
        """
        Get all stops for a trip
        """
        trip = self.get_object()
        stops = trip.stops.all()
        serializer = TripStopSerializer(stops, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """
        Get all events for a trip
        """
        trip = self.get_object()
        events = trip.events.all()
        serializer = TripEventSerializer(events, many=True)
        return Response(serializer.data)


class TripStopViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TripStop model
    """
    queryset = TripStop.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TripStopCreateSerializer
        return TripStopSerializer
    
    def get_queryset(self):
        queryset = TripStop.objects.all()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        # Filter by stop type
        stop_type = self.request.query_params.get('stop_type')
        if stop_type:
            queryset = queryset.filter(stop_type=stop_type)
        
        # Filter by completion status
        is_completed = self.request.query_params.get('is_completed')
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
        
        return queryset.order_by('trip', 'stop_order')
    
    @action(detail=True, methods=['post'])
    def arrive(self, request, pk=None):
        """
        Mark arrival at a stop
        """
        stop = self.get_object()
        stop.actual_arrival = timezone.now()
        stop.save()
        
        serializer = TripStopSerializer(stop)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def depart(self, request, pk=None):
        """
        Mark departure from a stop
        """
        stop = self.get_object()
        stop.actual_departure = timezone.now()
        stop.is_completed = True
        stop.save()
        
        # Create stop completion event
        TripEvent.objects.create(
            trip=stop.trip,
            event_type='stop',
            event_time=stop.actual_departure,
            description=f'Completed {stop.get_stop_type_display()} at {stop.city}, {stop.state}'
        )
        
        serializer = TripStopSerializer(stop)
        return Response(serializer.data)


class TripEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TripEvent model
    """
    queryset = TripEvent.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TripEventCreateSerializer
        return TripEventSerializer
    
    def get_queryset(self):
        queryset = TripEvent.objects.all()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        return queryset.order_by('-event_time')
