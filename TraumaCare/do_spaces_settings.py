# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

AWS_ACCESS_KEY_ID = 'DO801Z27G33R39LYHTC9' 
AWS_SECRET_ACCESS_KEY = 'SVVhNkLUM/YyWDEnf1Is4JHYgiMAlJ86NL/z7REzPg8'

AWS_STORAGE_BUCKET_NAME = 'traumacaremedia'
AWS_S3_ENDPOINT_URL = 'https://blr1.digitaloceanspaces.com'
# I enabled the CDN, so you get a custom domain. Use the end point in the AWS_S3_CUSTOM_DOMAIN setting. 
AWS_S3_CUSTOM_DOMAIN = 'traumacaremedia.blr1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_DEFAULT_ACL = 'x-amz-acl'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'TraumaCare.Constant.backends.MediaStorage'

# Use AWS_S3_ENDPOINT_URL here if you haven't enabled the CDN and got a custom domain. 
AWS_S3_SIGNATURE_VERSION = (
    "s3v4"
)

MEDIA_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'media')
MEDIA_ROOT = 'media/'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'