import os

from beethoven.settings.base import *


SECRET_KEY = 'd6$8l_h&96p4*h2=3*##o#k0ex^s7)xl80wyifzyo+1p_1fq!x'

DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
)

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/libs/jquery/jquery-1.11.1.min.js'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
