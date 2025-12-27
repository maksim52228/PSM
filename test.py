# views.py
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_upload(request):
    file = ContentFile(b"test content", name="test.txt")
    path = default_storage.save("test/test.txt", file)
    return HttpResponse(f"Saved to: {path}")

