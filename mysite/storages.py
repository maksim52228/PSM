from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class StaticStorage(S3Boto3Storage):
    location = 'staticfiles'  # Важно: должно совпадать с папкой в Supabase!
    default_acl = 'public-read'
    file_overwrite = False

    def url(self, name):
        # Используем кастомный URL Supabase с staticfiles
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}/staticfiles/{name}"
        return super().url(name)

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

    def url(self, name):
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}/media/{name}"
        return super().url(name)