



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

        paginator = client.get_paginator('list_objects')
        # dirs = client.list_objects(Bucket=bucket_name)['Contents']
        pages = paginator.paginate(Bucket='traumacare')

        # print(len(dirs))
        for page in pages:
            print(len(page['Contents']))
        # for d in dirs:
        #     print(d['Key'])


        self.stdout.write(self.style.SUCCESS('Successfully added'))