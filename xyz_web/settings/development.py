"""
@file Development settings for XYZ web.
"""

from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = []

SECRET_KEY = 'my-not-so-secret-development-key'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
