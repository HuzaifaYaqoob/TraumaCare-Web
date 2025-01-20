# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

AWS_ACCESS_KEY_ID='DO00TNX7NR4M6B8997MX' 
AWS_SECRET_ACCESS_KEY='Wa57orN6e+qVw6SjbhzsxaECkp9WvfKBEAmKsQtDUSM'

AWS_STORAGE_BUCKET_NAME='traumacaremedia'
# I enabled the CDN, so you get a custom domain. Use the end point in the AWS_S3_CUSTOM_DOMAIN setting. 
AWS_S3_CUSTOM_DOMAIN='traumacaremedia.blr1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_DEFAULT_ACL = 'x-amz-acl'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Use AWS_S3_ENDPOINT_URL here if you haven't enabled the CDN and got a custom domain. 
AWS_S3_ENDPOINT_URL = 'https://blr1.digitaloceanspaces.com'
AWS_S3_SIGNATURE_VERSION = (
    "s3v4"
)

MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'media')
MEDIA_ROOT = 'media/'

AWS_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_TIMEOUT = 70