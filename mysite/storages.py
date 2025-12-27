from storages.backends.s3boto3 import S3Boto3Storage


class SupabaseStorage(S3Boto3Storage):
    """
    Базовый класс для Supabase Storage
    """
    bucket_name = 'psm-media'
    location = ''
    file_overwrite = False
    default_acl = 'public-read'
    querystring_auth = False
    signature_version = 's3v4'  # Правильная версия подписи

    def __init__(self, *args, **kwargs):
        # Устанавливаем endpoint_url для Supabase
        self.endpoint_url = 'https://etcczklqfqdsomasmfcg.storage.supabase.co'
        super().__init__(*args, **kwargs)

    def url(self, name):
        # Кастомный URL для Supabase
        if self.location:
            return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{self.bucket_name}/{self.location}/{name}"
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{self.bucket_name}/{name}"


class MediaStorage(SupabaseStorage):
    location = 'media'
    file_overwrite = False


class StaticStorage(SupabaseStorage):
    location = 'staticfiles'
    file_overwrite = True