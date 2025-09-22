from django.db import models
from django.contrib.auth.models import AbstractUser

class Driver(AbstractUser):
    """
    Custom user model for drivers extending Django's built-in User
    """
    driver_license = models.CharField(max_length=20, unique=True)
    cdl_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    employee_id = models.CharField(max_length=20, blank=True)
    carrier_name = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='America/New_York')
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"

class Vehicle(models.Model):
    """
    Vehicle model for trucks and trailers
    """
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.license_plate}"
