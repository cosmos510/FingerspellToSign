import os
import boto3
from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        try:
            print("🚀 CoreConfig.ready() has started!")
            
            model_path = os.path.join(settings.BASE_DIR, 'model1.p')
            print(f"Checking model path: {model_path}")

            if os.path.exists(model_path):
                size = os.path.getsize(model_path)
                print(f"✅ Model file found locally at {model_path} (size: {size} bytes)")
            else:
                print("📦 Model not found locally. Downloading from S3...")

                aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
                aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
                bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
                s3_key = os.getenv('AWS_S3_KEY', 'model1.p')  # default to model1.p if not set

                if not all([aws_access_key_id, aws_secret_access_key, bucket_name]):
                    print("❌ Missing AWS environment variables. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_S3_BUCKET_NAME.")
                    return

                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                )

                os.makedirs(os.path.dirname(model_path), exist_ok=True)

                try:
                    with open(model_path, 'wb') as f:
                        s3.download_fileobj(bucket_name, s3_key, f)
                    print("✅ Model downloaded from S3.")
                except Exception as e:
                    print("❌ Failed to download model:", e)
        except Exception as e:
            print("❌ Exception in ready():", e)