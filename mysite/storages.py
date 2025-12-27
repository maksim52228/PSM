from storages.backends.s3 import S3Storage

class StaticStorage(S3Storage):
    location = 'staticfiles'
    file_overwrite = True
    querystring_auth = False

class MediaStorage(S3Storage):
    location = 'media'
    file_overwrite = False
    querystring_auth = False