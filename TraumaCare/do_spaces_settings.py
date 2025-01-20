
# AWS S3 Configuration for DigitalOcean Spaces
AWS_STORAGE_BUCKET_NAME='traumacaremedia'
AWS_ACCESS_KEY_ID="DO801EMJHULPRUDH6XM7"
AWS_SECRET_ACCESS_KEY="yfSmKRVpiROWxjo4aDyvKye7vHHnBSCdW83IMqN4rhg"
AWS_S3_ENDPOINT_URL='https://blr1.digitaloceanspaces.com'
AWS_LOCATION = f'https://traumacaremedia.blr1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATICFILES_STORAGE = 'TraumaCare.Constant.backends.StaticStorage'
STATIC_URL = f'https://traumacaremedia.blr1.digitaloceanspaces.com/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_FILE_STORAGE = 'TraumaCare.Constant.backends.MediaStorage'
MEDIA_URL = f'https://traumacaremedia.blr1.digitaloceanspaces.com/media/'

