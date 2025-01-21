import environ
env = environ.Env()


AWS_ACCESS_KEY_ID =env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME =env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = "https://blr1.digitaloceanspaces.com"  # Replace <region> (e.g., blr1)

# Media files storage
STATICFILES_STORAGE = "TraumaCare.Constant.backends.StaticStorage"
DEFAULT_FILE_STORAGE = "TraumaCare.Constant.backends.MediaStorage"

# URL settings
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL[8:]}/media/"
STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL[8:]}/static/"

# Optional: Cache settings for performance
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",  # Cache files for 1 day
}

# Optional: Enable file overwriting
AWS_QUERYSTRING_AUTH = False  # Removes query params from file URLs