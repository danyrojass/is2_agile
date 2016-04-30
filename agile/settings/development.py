# -*- coding: utf-8 -*-
from .production import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'agile_desarrollo',
        'USER': 'agile',
        'PASSWORD': 'admin123',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
}