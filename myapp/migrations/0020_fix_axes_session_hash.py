# myapp/migrations/0020_fix_axes_session_hash.py
from django.db import migrations

class Migration(migrations.Migration):
    # Убираем зависимость от axes — она не нужна для RunSQL
    dependencies = [
        ('myapp', '0019_delete_testimage'),  # ← последняя твоя миграция
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE axes_accesslog ADD COLUMN IF NOT EXISTS session_hash VARCHAR(64);",
            reverse_sql="ALTER TABLE axes_accesslog DROP COLUMN IF EXISTS session_hash;"
        ),
        migrations.RunSQL(
            "ALTER TABLE axes_accessattempt ADD COLUMN IF NOT EXISTS session_hash VARCHAR(64);",
            reverse_sql="ALTER TABLE axes_accessattempt DROP COLUMN IF EXISTS session_hash;"
        ),
        migrations.RunSQL(
            "ALTER TABLE axes_accesslog ALTER COLUMN session_hash DROP NOT NULL;",
            reverse_sql="SELECT 1;"
        ),
        migrations.RunSQL(
            "ALTER TABLE axes_accessattempt ALTER COLUMN session_hash DROP NOT NULL;",
            reverse_sql="SELECT 1;"
        ),
    ]