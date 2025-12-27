# mysite/storages.py
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'staticfiles'
    file_overwrite = True
    querystring_auth = False
    default_acl = None  # ← важно
    bucket_name = 'psm-media'

    def url(self, name):
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/psm-media/staticfiles/{name}"

    def _get_security_token(self):
        return None

    def _save(self, name, content):
        # Отключаем ACL при сохранении
        content_type = getattr(content, 'content_type', None)
        if content_type is None:
            content_type = self._guess_content_type(name)
        params = {'ContentType': content_type}
        # ❗ НЕ добавляем ACL
        self.bucket.Object(self._normalize_name(self._clean_name(name))).upload_fileobj(
            content, ExtraArgs=params
        )
        return name


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    querystring_auth = False
    default_acl = None
    bucket_name = 'psm-media'

    def url(self, name):
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/psm-media/media/{name}"

    def _get_security_token(self):
        return None

    def _save(self, name, content):
        content_type = getattr(content, 'content_type', None)
        if content_type is None:
            content_type = self._guess_content_type(name)
        params = {'ContentType': content_type}
        self.bucket.Object(self._normalize_name(self._clean_name(name))).upload_fileobj(
            content, ExtraArgs=params
        )
        return name