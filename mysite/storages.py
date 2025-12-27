from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    querystring_auth = False
    default_acl = None
    bucket_name = 'psm-media'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переопределяем host для Supabase
        self.endpoint_url = 'https://etcczklqfqdsomasmfcg.storage.supabase.co'


class StaticStorage(S3Boto3Storage):
    location = 'staticfiles'
    file_overwrite = True
    querystring_auth = False
    default_acl = None
    bucket_name = 'psm-media'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переопределяем host для Supabase
        self.endpoint_url = 'https://etcczklqfqdsomasmfcg.storage.supabase.co'