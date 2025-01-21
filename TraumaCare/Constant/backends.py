
from storages.backends.s3boto3 import S3Boto3Storage


# Storage for static files
class StaticStorage(S3Boto3Storage):
    location = 'static'
    file_overwrite = True
    default_acl = 'public-read'

# Storage for media files
class MediaStorage(S3Boto3Storage):
    location = 'media'
    # file_overwrite = False
    default_acl = "public-read"
