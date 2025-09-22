#!/bin/bash

# Full-Stack ELD Application Build Script

echo "🚛 Building ELD Assessment Application..."

# Build React Frontend
echo "📦 Building React Frontend..."
cd frontend
npm install
npm run build
cd ..

# Setup Django Backend
echo "🐍 Setting up Django Backend..."
cd driver_truck
python -m venv venv

# Activate virtual environment (adjust for your OS)
if [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

echo "✅ Build complete!"
echo ""
echo "🚀 To run the application:"
echo "Backend: cd driver_truck && python manage.py runserver"
echo "Frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Access:"
echo "React UI: http://localhost:3000"
echo "Django API: http://localhost:8000"