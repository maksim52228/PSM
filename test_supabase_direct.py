# upload_static_to_supabase.py
import os
import boto3
from botocore.client import Config
from django.conf import settings
from django.core.management import execute_from_command_line


def upload_static_files():
    print("Загружаем статические файлы Django в Supabase...")

    # 1. Сначала соберем статику локально
    print("1. Собираем статические файлы локально...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    # Импортируем Django после установки настроек
    import django
    django.setup()

    # Создаем временную папку для статики
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    original_static_root = settings.STATIC_ROOT

    try:
        # Временно меняем STATIC_ROOT
        settings.STATIC_ROOT = temp_dir

        # Собираем статику
        from django.core.management import call_command
        call_command('collectstatic', '--noinput', '--clear')

        print(f"2. Собрано файлов в {temp_dir}")

        # 2. Загружаем в Supabase
        print("3. Загружаем файлы в Supabase...")

        s3 = boto3.client(
            's3',
            endpoint_url='https://etcczklqfqdsomasmfcg.storage.supabase.co',
            region_name='eu-west-3',
            aws_access_key_id='0d1f99967b6d9bbf47d92583ed12e203',
            aws_secret_access_key='a0545ae325dff7da7ff3f80c22d203a7ae74275f3a60568a77e0949baff38e71',
            config=Config(
                s3={'addressing_style': 'path'},
                signature_version='s3v4'
            )
        )

        # Рекурсивно загружаем файлы
        uploaded = 0
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                local_path = os.path.join(root, file)
                # Создаем путь в Supabase
                relative_path = os.path.relpath(local_path, temp_dir)
                s3_key = f'static/{relative_path}'.replace('\\', '/')

                # Определяем Content-Type
                content_type = 'application/octet-stream'
                if file.endswith('.css'):
                    content_type = 'text/css'
                elif file.endswith('.js'):
                    content_type = 'application/javascript'
                elif file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico')):
                    content_type = f'image/{file.split(".")[-1]}'

                # Загружаем файл
                with open(local_path, 'rb') as f:
                    s3.put_object(
                        Bucket='psm-media',
                        Key=s3_key,
                        Body=f.read(),
                        ContentType=content_type,
                        ACL='public-read'
                    )

                uploaded += 1
                if uploaded % 10 == 0:
                    print(f"  Загружено {uploaded} файлов...")

        print(f"\n✅ Загружено {uploaded} файлов в Supabase!")
        print(f"\n📁 Ваши статические файлы доступны по адресу:")
        print(f"   https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/psm-media/static/")

    finally:
        # Восстанавливаем настройки
        settings.STATIC_ROOT = original_static_root
        # Удаляем временную папку
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    upload_static_files()