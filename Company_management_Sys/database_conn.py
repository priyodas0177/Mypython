#!/usr/bin/env python
import os
import django
from django.db import connection

# Set your Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello.settings')
django.setup()

# Test database connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    print("✅ Database connection successful:", result)
except Exception as e:
    print("❌ Database connection failed:", e)
