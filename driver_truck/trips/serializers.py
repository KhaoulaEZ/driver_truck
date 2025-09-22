from rest_framework import serializers
from .models import Trip, TripStop, TripEvent
from drivers.serializers import DriverListSerializer


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for Trip model
    """
    driver_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    duration_planned_hours = serializers.ReadOnlyField()
    duration_actual_hours = serializers.ReadOnlyField()
    origin_full_address = serializers.ReadOnlyField()
    destination_full_address = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Trip
        fields = [
            'id', 'driver', 'driver_name', 'trip_number',
            'origin_address', 'origin_city', 'origin_state', 'origin_zip',
            'origin_latitude', 'origin_longitude', 'origin_full_address',
            'destination_address', 'destination_city', 'destination_state', 'destination_zip',
            'destination_latitude', 'destination_longitude', 'destination_full_address',
            'planned_start_time', 'planned_end_time', 'duration_planned_hours',
            'actual_start_time', 'actual_end_time', 'duration_actual_hours',
            'estimated_distance', 'actual_distance', 'load_description', 'load_weight',
            'status', 'status_display', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
    
    def get_driver_name(self, obj):
        return obj.driver.get_full_name() or obj.driver.username
    
    def get_status_display(self, obj):
        return obj.get_status_display()


class TripCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating trips
    """
    class Meta:
        model = Trip
        fields = [
            'driver', 'trip_number', 'origin_address', 'origin_city', 
            'origin_state', 'origin_zip', 'origin_latitude', 'origin_longitude',
            'destination_address', 'destination_city', 'destination_state', 
            'destination_zip', 'destination_latitude', 'destination_longitude',
            'planned_start_time', 'planned_end_time', 'estimated_distance',
            'load_description', 'load_weight', 'notes'
        ]
    
    def validate(self, data):
        """
        Validate trip data
        """
        planned_start = data.get('planned_start_time')
        planned_end = data.get('planned_end_time')
        
        if planned_end and planned_start and planned_end <= planned_start:
            raise serializers.ValidationError(
                "Planned end time must be after planned start time."
            )
        
        return data


class TripListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for trip list views
    """
    driver_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    origin_destination = serializers.SerializerMethodField()
    
    class Meta:
        model = Trip
        fields = [
            'id', 'trip_number', 'driver_name', 'origin_destination',
            'planned_start_time', 'planned_end_time', 'status', 'status_display',
            'estimated_distance', 'load_description'
        ]
    
    def get_driver_name(self, obj):
        return obj.driver.get_full_name() or obj.driver.username
    
    def get_status_display(self, obj):
        return obj.get_status_display()
    
    def get_origin_destination(self, obj):
        return f"{obj.origin_city}, {obj.origin_state} → {obj.destination_city}, {obj.destination_state}"


class TripStopSerializer(serializers.ModelSerializer):
    """
    Serializer for TripStop model
    """
    stop_type_display = serializers.SerializerMethodField()
    full_address = serializers.ReadOnlyField()
    trip_number = serializers.SerializerMethodField()
    
    class Meta:
        model = TripStop
        fields = [
            'id', 'trip', 'trip_number', 'stop_type', 'stop_type_display',
            'stop_order', 'address', 'city', 'state', 'zip_code',
            'full_address', 'latitude', 'longitude',
            'planned_arrival', 'planned_departure',
            'actual_arrival', 'actual_departure',
            'description', 'notes', 'is_completed', 'created_at'
        ]
    
    def get_stop_type_display(self, obj):
        return obj.get_stop_type_display()
    
    def get_trip_number(self, obj):
        return obj.trip.trip_number


class TripStopCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating trip stops
    """
    class Meta:
        model = TripStop
        fields = [
            'trip', 'stop_type', 'stop_order', 'address', 'city', 'state',
            'zip_code', 'latitude', 'longitude', 'planned_arrival',
            'planned_departure', 'description', 'notes'
        ]
    
    def validate(self, data):
        """
        Validate trip stop data
        """
        planned_arrival = data.get('planned_arrival')
        planned_departure = data.get('planned_departure')
        
        if planned_departure and planned_arrival and planned_departure <= planned_arrival:
            raise serializers.ValidationError(
                "Planned departure must be after planned arrival."
            )
        
        return data


class TripEventSerializer(serializers.ModelSerializer):
    """
    Serializer for TripEvent model
    """
    event_type_display = serializers.SerializerMethodField()
    trip_number = serializers.SerializerMethodField()
    
    class Meta:
        model = TripEvent
        fields = [
            'id', 'trip', 'trip_number', 'event_type', 'event_type_display',
            'event_time', 'location', 'latitude', 'longitude',
            'description', 'additional_data', 'created_at'
        ]
    
    def get_event_type_display(self, obj):
        return obj.get_event_type_display()
    
    def get_trip_number(self, obj):
        return obj.trip.trip_number


class TripEventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating trip events
    """
    class Meta:
        model = TripEvent
        fields = [
            'trip', 'event_type', 'event_time', 'location',
            'latitude', 'longitude', 'description', 'additional_data'
        ]