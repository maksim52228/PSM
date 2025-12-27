import boto3
from botocore.client import Config

# === ВАШИ ДАННЫЕ ИЗ .env ===
ACCESS_KEY="0d1f99967b6d9bbf47d92583ed12e203"
SECRET_KEY="a0545ae325dff7da7ff3f80c22d203a7ae74275f3a60568a77e0949baff38e71"
ENDPOINT = "https://etcczklqfqdsomasmfcg.storage.supabase.co/storage/v1/s3"
BUCKET = "psm-media"

print("🔍 Подключаемся к Supabase Storage...")

s3 = boto3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='eu-west-3',
    config=Config(signature_version='s3v4', s3={'addressing_style': 'path'})
)

try:
    print("📤 Загружаем тестовый файл...")
    s3.put_object(
        Bucket=BUCKET,
        Key='test_from_pycharm2.txt',
        Body=b'This file was uploaded from PyCharm directly via boto3!',
        ACL='public-read'
    )
    public_url = f"https://etcczklqfqdsomasmfcg.supabase.co/storage/v1/object/public/{BUCKET}/test_from_pycharm2.txt"
    print("✅ УСПЕХ!")
    print("Файл доступен по ссылке:")
    print(public_url)
except Exception as e:
    print("❌ ОШИБКА:")
    print(str(e))