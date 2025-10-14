#!/bin/bash

# Wait for database to be ready (if using external DB)
echo "Starting Django development server..."

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
exec python manage.py runserver 0.0.0.0:8000