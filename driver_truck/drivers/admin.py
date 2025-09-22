from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Driver, Vehicle


@admin.register(Driver)
class DriverAdmin(UserAdmin):
    """
    Custom admin for Driver model
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'driver_license', 'cdl_number', 'carrier_name', 'is_active'
    ]
    list_filter = ['is_active', 'carrier_name', 'timezone']
    search_fields = ['username', 'email', 'driver_license', 'cdl_number', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Driver Information', {
            'fields': (
                'driver_license',
                'cdl_number',
                'phone_number',
                'employee_id',
                'carrier_name',
                'timezone'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Driver Information', {
            'fields': (
                'driver_license',
                'cdl_number',
                'phone_number',
                'employee_id',
                'carrier_name',
                'timezone'
            )
        }),
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Admin for Vehicle model
    """
    list_display = [
        'license_plate', 'vin', 'make', 'model', 'year', 
        'assigned_driver', 'is_active'
    ]
    list_filter = ['make', 'year', 'is_active']
    search_fields = ['license_plate', 'vin', 'make', 'model']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('license_plate', 'vin', 'make', 'model', 'year')
        }),
        ('Assignment', {
            'fields': ('assigned_driver', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
