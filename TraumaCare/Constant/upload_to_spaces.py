import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import NoCredentialsError
import os
from botocore.config import Config
import botocore


# Manual file upload to DigitalOcean Spaces
def upload_file_to_spaces(file_path):
    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        config=botocore.config.Config(s3={'addressing_style': 'virtual'}, connect_timeout=60, read_timeout=120, retries={'max_attempts': 5}, tcp_keepalive=True),
        region_name='blr1',
        
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    print(client)

    # client.put_object(
    #             Bucket=settings.AWS_STORAGE_BUCKET_NAME, 
    #             Key=file_path, 
    #             Body=b'Hello, World!',
    #             ACL='private',
    #             Metadata={
    #                 'x-amz-meta-my-key': 'your-value'
    #             }
    #         )
    try:
        print(os.path.curdir)
        # Define key for the uploaded file in Spaces
        key = f'{os.path.basename(file_path)}'
        print(key)

        with open(file_path, 'rb') as data:
            print(data)
            # Use upload_fileobj without ContentLength
            # client.upload_fileobj(
            #     Fileobj=data,
            #     Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            #     Key=key,
            #     ExtraArgs={
            #         'ContentType': 'application/octet-stream',  # Set appropriate content type
            #         'ACL': 'public-read'  # Optional: Set file access permissions
            #     }
            # )
            part = client.upload_part(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, 
                Key=key, 
                PartNumber=1,
                UploadId='1',
                Body=data.read()
                )


        print(f"File uploaded successfully to: {key}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error: {e}")