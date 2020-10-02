"""
@file Production settings

Requires the following environment variables to be set:
- SECRET_KEY
- MYSQL_DATABASE
- MYSQL_USER
- MYSQL_USER_PASSWORD
"""

from os import environ
import pymysql
from .base import *  # noqa: F401, F403

pymysql.install_as_MySQLdb()

get_env = environ.get  # Just alias with shorter name.

DEBUG = False
SECRET_KEY = get_env("SECRET_KEY")

ALLOWED_HOSTS = ['xyz.nabla.no']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_env("MYSQL_DATABASE", "xyz"),
        "USER": get_env("MYSQL_USER", "xyz"),
        "PASSWORD": get_env("MYSQL_USER_PASSWORD"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"timestamp": {"format": "%(asctime)s %(message)s"}},
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": get_env(
                "DJANGO_LOG_PATH", "/var/log/django/nablaweb/error.log"
            ),
            "formatter": "timestamp",
        },
    },
    "loggers": {"django": {"handlers": ["file"], "level": "ERROR", "propagate": True}},
}