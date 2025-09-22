from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

Driver = get_user_model()


class TripStatus(models.TextChoices):
    """
    Trip status options
    """
    PLANNED = 'planned', 'Planned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class Trip(models.Model):
    """
    Main trip/route model
    """
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    
    # Trip identification
    trip_number = models.CharField(max_length=50, unique=True)
    
    # Route information
    origin_address = models.CharField(max_length=300)
    origin_city = models.CharField(max_length=100)
    origin_state = models.CharField(max_length=50)
    origin_zip = models.CharField(max_length=10)
    
    destination_address = models.CharField(max_length=300)
    destination_city = models.CharField(max_length=100)
    destination_state = models.CharField(max_length=50)
    destination_zip = models.CharField(max_length=10)
    
    # Coordinates (for mapping)
    origin_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    origin_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    destination_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    destination_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Trip timing
    planned_start_time = models.DateTimeField()
    planned_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Trip details
    estimated_distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Estimated distance in miles"
    )
    actual_distance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual distance traveled in miles"
    )
    
    # Load information
    load_description = models.CharField(max_length=200, blank=True)
    load_weight = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Load weight in pounds"
    )
    
    # Status and tracking
    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.PLANNED
    )
    
    # Notes
    notes = models.TextField(blank=True)
    
    # System tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trips'
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
        ordering = ['-planned_start_time']
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.driver.username}"
    
    @property
    def is_active(self):
        """Check if trip is currently in progress"""
        return self.status == TripStatus.IN_PROGRESS
    
    @property
    def duration_planned_hours(self):
        """Calculate planned duration in hours"""
        if self.planned_end_time and self.planned_start_time:
            delta = self.planned_end_time - self.planned_start_time
            return round(delta.total_seconds() / 3600, 2)
        return 0
    
    @property
    def duration_actual_hours(self):
        """Calculate actual duration in hours"""
        if self.actual_end_time and self.actual_start_time:
            delta = self.actual_end_time - self.actual_start_time
            return round(delta.total_seconds() / 3600, 2)
        return 0
    
    @property
    def origin_full_address(self):
        """Get formatted origin address"""
        return f"{self.origin_address}, {self.origin_city}, {self.origin_state} {self.origin_zip}"
    
    @property
    def destination_full_address(self):
        """Get formatted destination address"""
        return f"{self.destination_address}, {self.destination_city}, {self.destination_state} {self.destination_zip}"


class TripStop(models.Model):
    """
    Intermediate stops during a trip
    """
    STOP_TYPES = [
        ('fuel', 'Fuel Stop'),
        ('rest', 'Rest Stop'),
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
        ('inspection', 'Inspection'),
        ('other', 'Other'),
    ]
    
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='stops'
    )
    
    # Stop details
    stop_type = models.CharField(max_length=20, choices=STOP_TYPES)
    stop_order = models.PositiveIntegerField(default=1)
    
    # Location
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    # Coordinates
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Timing
    planned_arrival = models.DateTimeField()
    planned_departure = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    actual_departure = models.DateTimeField(null=True, blank=True)
    
    # Stop details
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # Completion status
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trip_stops'
        verbose_name = 'Trip Stop'
        verbose_name_plural = 'Trip Stops'
        ordering = ['trip', 'stop_order']
        unique_together = ['trip', 'stop_order']
    
    def __str__(self):
        return f"{self.trip.trip_number} - Stop {self.stop_order} ({self.get_stop_type_display()})"
    
    @property
    def full_address(self):
        """Get formatted full address"""
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"


class TripEvent(models.Model):
    """
    Events that occur during a trip (fuel stops, inspections, etc.)
    """
    EVENT_TYPES = [
        ('start', 'Trip Started'),
        ('stop', 'Stop Completed'),
        ('fuel', 'Fuel Purchase'),
        ('inspection', 'Vehicle Inspection'),
        ('breakdown', 'Vehicle Breakdown'),
        ('delay', 'Delay Encountered'),
        ('complete', 'Trip Completed'),
        ('other', 'Other Event'),
    ]
    
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='events'
    )
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_time = models.DateTimeField(default=timezone.now)
    
    # Location where event occurred
    location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Event details
    description = models.TextField()
    
    # Additional data (JSON for flexibility)
    additional_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional event data (fuel amount, cost, etc.)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trip_events'
        verbose_name = 'Trip Event'
        verbose_name_plural = 'Trip Events'
        ordering = ['-event_time']
    
    def __str__(self):
        return f"{self.trip.trip_number} - {self.get_event_type_display()} - {self.event_time.strftime('%Y-%m-%d %H:%M')}"
