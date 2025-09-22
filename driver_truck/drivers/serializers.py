from rest_framework import serializers
from .models import Driver, Vehicle


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for Driver model
    """
    password = serializers.CharField(write_only=True, min_length=8, help_text="Password for the driver account")
    
    class Meta:
        model = Driver
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'driver_license', 'cdl_number', 'phone_number', 
            'employee_id', 'carrier_name', 'timezone',
            'is_active', 'date_joined', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'driver_license': {'help_text': 'Driver license number (required)'},
            'username': {'help_text': 'Unique username for login'},
            'email': {'help_text': 'Email address'}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        driver = Driver.objects.create_user(**validated_data)
        driver.set_password(password)
        driver.save()
        return driver
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DriverListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for driver list views
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Driver
        fields = [
            'id', 'username', 'full_name', 'driver_license',
            'carrier_name', 'is_active'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for Vehicle model
    """
    assigned_driver_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'vin', 'make', 'model', 'year',
            'assigned_driver', 'assigned_driver_name', 'is_active', 'notes'
        ]
    
    def get_assigned_driver_name(self, obj):
        if obj.assigned_driver:
            return obj.assigned_driver.get_full_name() or obj.assigned_driver.username
        return None


class VehicleListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for vehicle list views
    """
    assigned_driver_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'make', 'model', 'year',
            'assigned_driver_name', 'is_active'
        ]
    
    def get_assigned_driver_name(self, obj):
        if obj.assigned_driver:
            return obj.assigned_driver.get_full_name() or obj.assigned_driver.username
        return None