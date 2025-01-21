import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import NoCredentialsError
import os
from botocore.config import Config
import botocore


# Manual file upload to DigitalOcean Spaces
def upload_file_to_spaces(file_path, bucket_name=None, object_key=None):
    print('upload_file_to_spaces')
    # try:
    bucket_name = bucket_name or settings.AWS_STORAGE_BUCKET_NAME
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

    # Upload the file
    object_key = file_path
    print(object_key)

    with open(file_path, 'rb') as file_data:
        client.upload_fileobj(
            Fileobj=file_data,
            Bucket=bucket_name,
            Key=object_key,
            ExtraArgs={
                'ContentType': 'application/octet-stream',
                'ACL': 'public-read'
            }
        )

    if os.path.exists(file_path):
        os.remove(file_path)
    # Construct the file URL
    file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{bucket_name}/{object_key}"
    print(f"File uploaded successfully: {file_url}")
    print('upload_file_to_spaces')

    return file_url

    # except NoCredentialsError:
    #     print("Error: Credentials not available.")
    # except ClientError as e:
    #     print(f"Client error occurred: {e}")
    # except Exception as e:
    #     print(f"Unexpected error: {e}")
    