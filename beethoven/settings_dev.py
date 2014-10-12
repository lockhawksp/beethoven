from beethoven.settings_base import INSTALLED_APPS


SECRET_KEY = 'd6$8l_h&96p4*h2=3*##o#k0ex^s7)xl80wyifzyo+1p_1fq!x'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)

WSGI_APPLICATION = 'beethoven.wsgi.application'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/libs/jquery/jquery-1.11.1.min.js'
}

SSLIFY_DISABLE = True
