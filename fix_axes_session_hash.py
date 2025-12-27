# fix_axes_session_hash.py
import os
import django
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def fix_session_hash_nullable():
    with connection.cursor() as cursor:
        # Делаем колонку session_hash допускающей NULL
        cursor.execute("""
            ALTER TABLE axes_accesslog
            ALTER COLUMN session_hash DROP NOT NULL;
        """)
        print("✅ Колонка session_hash теперь допускает NULL")

if __name__ == "__main__":
    fix_session_hash_nullable()