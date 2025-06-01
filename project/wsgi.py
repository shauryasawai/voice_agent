# ================================
# project/wsgi.py (Updated for Vercel)
# ================================

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# Vercel serverless function handler
app = application