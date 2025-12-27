from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'staticfiles'
    default_acl = 'public-read'
    file_overwrite = True  # Полезно для статики

    def url(self, name):
        # Supabase публичный URL для статических файлов
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{self.bucket_name}/staticfiles/{name}"


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    querystring_auth = False

    def url(self, name):
        # Supabase публичный URL для медиафайлов
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{self.bucket_name}/media/{name}"

    def get_object_parameters(self, name):
        # Добавляем ACL при загрузке файла
        params = super().get_object_parameters(name)
        params['ACL'] = 'public-read'
        return params