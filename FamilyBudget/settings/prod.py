import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
SECRET_KEY = config('SECRET_KEY')

MEDIA_ROOT = os.path.join(BASE_DIR, '/path/')
MEDIA_URL = '/path/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/') 
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD':config('DATABASE_PASSWORD'),
        'PORT':config('DATABASE_PORT',default=3306,cast=int),
        'HOST':config('DATABASE_HOST',cast=str),
    }
}
