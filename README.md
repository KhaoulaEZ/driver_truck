# Driver Truck ELD System

Electronic Logging Device (ELD) tracker built with Django and React.

## Features
- Driver management and authentication
- Daily duty logs tracking
- Trip management
- Hours of Service (HoS) compliance

## Setup

### Backend (Django)
```bash
cd driver_truck
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## Tech Stack
- **Backend**: Django, Django REST Framework, SQLite
- **Frontend**: React, Axios