import os

import dj_database_url


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'beethoven.heroku_wsgi.application'

DATABASES = {
    'default': dj_database_url.config()
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = 'staticfiles'
