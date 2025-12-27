from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    querystring_auth = False

    def url(self, name):
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/psm-media/media/{name}"

    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)
        params['ACL'] = 'public-read'
        return params


class StaticStorage(S3Boto3Storage):
    location = 'staticfiles'
    default_acl = 'public-read'
    file_overwrite = True

    def url(self, name):
        return f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/psm-media/staticfiles/{name}"