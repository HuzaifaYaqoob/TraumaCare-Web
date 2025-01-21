



from django.core.management.base import BaseCommand
import os
import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError, ClientError

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        session = boto3.session.Session()
        client = session.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            config=boto3.session.Config(
                s3={'addressing_style': 'virtual'},
                connect_timeout=60,
                read_timeout=120,
                retries={'max_attempts': 5},
                tcp_keepalive=True
            ),
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        local_dir = "media/"
        spaces_dir = "media/"
        for root, dirs, files in os.walk('media/'):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(local_file_path, local_dir)
                spaces_file_path = os.path.join(spaces_dir, relative_path).replace("\\", "/")  # For Windows compatibility

                print(local_file_path)
                with open(local_file_path, "rb") as data:
                    client.upload_fileobj(
                        Fileobj=data,
                        Bucket=bucket_name,
                        Key=spaces_file_path,
                        ExtraArgs={"ACL": "public-read"}
                    )
                print(f"Uploaded: {local_file_path} to {spaces_file_path}")



        self.stdout.write(self.style.SUCCESS('Successfully added'))