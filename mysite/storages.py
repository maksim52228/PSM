from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class SupabaseStorage(S3Boto3Storage):
    """
    Базовый класс для Supabase Storage
    """
    endpoint_url = 'https://etcczklqfqdsomasmfcg.storage.supabase.co'
    bucket_name = 'psm-media'
    custom_domain = f'etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{bucket_name}'
    file_overwrite = False
    default_acl = 'public-read'  # Supabase требует public-read для публичных файлов
    location = ''

    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = self.bucket_name
        kwargs['endpoint_url'] = self.endpoint_url
        super().__init__(*args, **kwargs)

    def _get_security_token(self):
        # Отключаем STS токены для Supabase
        return None

    def _normalize_name(self, name):
        # Убедимся, что путь корректный
        if self.location:
            name = f"{self.location}/{name}"
        return name

    def url(self, name):
        # Используем кастомный домен для публичных URL
        if self.custom_domain:
            return f"https://{self.custom_domain}/{self.location}/{name}"
        return super().url(name)


class MediaStorage(SupabaseStorage):
    location = 'media'
    file_overwrite = False


class StaticStorage(SupabaseStorage):
    location = 'staticfiles'
    file_overwrite = True  # Статические файлы можно перезаписывать