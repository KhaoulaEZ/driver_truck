from django.contrib import admin
from .models import Trip, TripStop, TripEvent


class TripStopInline(admin.TabularInline):
    """
    Inline admin for TripStop
    """
    model = TripStop
    extra = 0
    fields = [
        'stop_order', 'stop_type', 'city', 'state',
        'planned_arrival', 'planned_departure', 'is_completed'
    ]


class TripEventInline(admin.TabularInline):
    """
    Inline admin for TripEvent
    """
    model = TripEvent
    extra = 0
    fields = ['event_type', 'event_time', 'location', 'description']
    readonly_fields = ['event_time']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Admin for Trip model
    """
    list_display = [
        'trip_number', 'driver', 'origin_city', 'destination_city',
        'planned_start_time', 'status', 'estimated_distance'
    ]
    list_filter = ['status', 'planned_start_time', 'origin_state', 'destination_state']
    search_fields = [
        'trip_number', 'driver__username', 'origin_city', 
        'destination_city', 'load_description'
    ]
    readonly_fields = [
        'duration_planned_hours', 'duration_actual_hours',
        'is_active', 'created_at', 'updated_at'
    ]
    
    inlines = [TripStopInline, TripEventInline]
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'driver', 'status')
        }),
        ('Origin', {
            'fields': (
                'origin_address', 'origin_city', 'origin_state', 'origin_zip',
                'origin_latitude', 'origin_longitude'
            )
        }),
        ('Destination', {
            'fields': (
                'destination_address', 'destination_city', 'destination_state', 'destination_zip',
                'destination_latitude', 'destination_longitude'
            )
        }),
        ('Timing', {
            'fields': (
                'planned_start_time', 'planned_end_time', 'duration_planned_hours',
                'actual_start_time', 'actual_end_time', 'duration_actual_hours'
            )
        }),
        ('Distance and Load', {
            'fields': ('estimated_distance', 'actual_distance', 'load_description', 'load_weight')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'planned_start_time'


@admin.register(TripStop)
class TripStopAdmin(admin.ModelAdmin):
    """
    Admin for TripStop model
    """
    list_display = [
        'trip', 'stop_order', 'stop_type', 'city', 'state',
        'planned_arrival', 'is_completed'
    ]
    list_filter = ['stop_type', 'is_completed', 'state']
    search_fields = ['trip__trip_number', 'city', 'address', 'description']
    
    fieldsets = (
        ('Stop Information', {
            'fields': ('trip', 'stop_order', 'stop_type', 'description')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Timing', {
            'fields': ('planned_arrival', 'planned_departure', 'actual_arrival', 'actual_departure')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(TripEvent)
class TripEventAdmin(admin.ModelAdmin):
    """
    Admin for TripEvent model
    """
    list_display = [
        'trip', 'event_type', 'event_time', 'location', 'description'
    ]
    list_filter = ['event_type', 'event_time']
    search_fields = ['trip__trip_number', 'location', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('trip', 'event_type', 'event_time', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Additional Data', {
            'fields': ('additional_data',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'event_time'
