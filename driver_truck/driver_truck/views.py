from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'index.html')

def demo(request):
    return render(request, 'demo.html')

@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def api_status(request):
    """Simple API status endpoint"""
    return JsonResponse({
        'status': 'online',
        'message': 'ELD Assessment API is running',
        'endpoints': {
            'drivers': '/api/drivers/',
            'logs': '/api/logs/',
            'trips': '/api/trips/',
            'schema': '/schema/',
            'admin': '/admin/'
        }
    })