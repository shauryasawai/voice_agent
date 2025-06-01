#!/bin/bash

echo "BUILD START"

# Install dependencies locally for Vercel's lambda build
python3.9 -m pip install -r requirements.txt --target ./package

# Optional zip creation (can be removed unless you use it explicitly)
cd package
zip -r9 ../function.zip .
cd ..

zip -r9 function.zip .

# Collect static files into staticfiles_build
python3.9 manage.py collectstatic --noinput --clear

# Create the output folder for static build
mkdir -p staticfiles_build

# Copy templates and required Django files to staticfiles_build (so Vercel includes them)
cp -r base staticfiles_build/base
cp -r project staticfiles_build/project
cp -r manage.py staticfiles_build/

echo "BUILD END"
