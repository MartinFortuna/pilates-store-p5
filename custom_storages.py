from django.conf import settings
from storages.backends.s3boto3 import S3boto3Storage


class StaticStorage(S3boto3Storage):
    location = setting.STATICFILES_LOCATION


class MadiaStorage(S3boto3Storage):
    location = setting.MEDIAFILES_LOCATION
