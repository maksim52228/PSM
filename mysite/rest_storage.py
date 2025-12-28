# mysite/rest_storage.py
import os
import requests
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, bucket=None, base_path=None):
        self.bucket = bucket or getattr(settings, 'SUPABASE_BUCKET', 'psm-media')
        self.base_path = base_path or ''
        self.project_ref = getattr(settings, 'SUPABASE_PROJECT_REF', 'etcczklqfqdsomasmfcg')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # ← используйте отдельную переменную
        if not self.service_role_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required")

    def _get_url(self, name):
        path = f"{self.base_path}/{name}".lstrip('/')
        return f"https://{self.project_ref}.supabase.co/storage/v1/object/{self.bucket}/{path}"

    def _get_public_url(self, name):
        path = f"{self.base_path}/{name}".lstrip('/')
        return f"https://{self.project_ref}.supabase.co/storage/v1/object/public/{self.bucket}/{path}"

    def _save(self, name, content):
        url = self._get_url(name)
        headers = {
            'Authorization': f'Bearer {self.service_role_key}',
            'Content-Type': getattr(content, 'content_type', 'application/octet-stream'),
            'x-upsert': 'true',
        }
        content.seek(0)
        response = requests.put(url, data=content.read(), headers=headers)
        response.raise_for_status()
        return name

    def url(self, name):
        return self._get_public_url(name)

    def exists(self, name):
        # Для простоты всегда возвращаем False — безопасно для collectstatic
        return False

    def delete(self, name):
        url = self._get_url(name)
        headers = {'Authorization': f'Bearer {self.service_role_key}'}
        requests.delete(url, headers=headers)

class StaticStorage(SupabaseStorage):
    def __init__(self):
        super().__init__(base_path='staticfiles')

class MediaStorage(SupabaseStorage):
    def __init__(self):
        super().__init__(base_path='media')