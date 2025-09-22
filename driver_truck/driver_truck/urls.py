"""driver_truck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from . import views

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('demo/', views.demo, name='demo'),
    path('api/status/', views.api_status, name='api-status'),
    path('api/csrf/', views.get_csrf_token, name='csrf-token'),
    
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/drivers/', include('drivers.urls')),
    path('api/logs/', include('logs.urls')),
    path('api/trips/', include('trips.urls')),
    
    # DRF auth endpoints
    path('api-auth/', include('rest_framework.urls')),
    
    # API documentation with drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
