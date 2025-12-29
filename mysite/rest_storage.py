# mysite/rest_storage.py
import os
import requests
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
from decouple import config
@deconstructible
class MediaStorage(Storage):
    def __init__(self):
        self.bucket = getattr(settings, 'SUPABASE_BUCKET', 'psm-media')
        self.project_ref = getattr(settings, 'SUPABASE_PROJECT_ID', 'etcczklqfqdsomasmfcg')
        self.service_role_key = config('SUPABASE_SERVICE_ROLE_KEY')
        if not self.service_role_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required")

    def _get_upload_url(self, name):
        # Путь в бакете: media/filename.jpg
        return f"https://{self.project_ref}.supabase.co/storage/v1/object/{self.bucket}/media/{name}"

    def _get_public_url(self, name):
        return f"https://{self.project_ref}.supabase.co/storage/v1/object/public/{self.bucket}/media/{name}"

    def _save(self, name, content):
        url = self._get_upload_url(name)
        headers = {
            'Authorization': f'Bearer {self.service_role_key}',
            'Content-Type': getattr(content, 'content_type', 'application/octet-stream'),
            'x-upsert': 'true',
        }
        content.seek(0)
        file_data = content.read()
        response = requests.put(url, data=file_data, headers=headers, timeout=30)
        response.raise_for_status()
        return name

    def url(self, name):
        return self._get_public_url(name)

    def exists(self, name):
        return False  # безопасно для Django

    def delete(self, name):
        url = self._get_upload_url(name)
        headers = {'Authorization': f'Bearer {self.service_role_key}'}
        requests.delete(url, headers=headers)