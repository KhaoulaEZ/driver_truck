# Backend - Django REST API

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## API Endpoints

| Endpoint | Description | Methods |
|----------|-------------|---------|
| `/api/drivers/drivers/` | Driver management | GET, POST, PUT, DELETE |
| `/api/drivers/vehicles/` | Vehicle management | GET, POST, PUT, DELETE |
| `/api/logs/duty-logs/` | Duty status logging | GET, POST, PUT, DELETE |
| `/api/logs/hos-violations/` | HoS violations | GET, POST |
| `/api/logs/daily-summaries/` | Daily log summaries | GET, POST |
| `/api/trips/trips/` | Trip management | GET, POST, PUT, DELETE |
| `/api/trips/trip-stops/` | Trip stops | GET, POST, PUT, DELETE |
| `/api/trips/trip-events/` | Trip events | GET, POST, PUT, DELETE |

## Tech Stack
- Django 5.2.6
- Django REST Framework 3.16.1
- SQLite Database
- Python 3.11

## Future Features
- JWT token authentication
- Real-time GPS tracking
- Advanced reporting dashboard
- Email notifications for violations
- Data export to Excel/PDF