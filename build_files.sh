#!/bin/bash

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🧼 Cleaning old static files..."
rm -rf staticfiles

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete. Static files are ready."
