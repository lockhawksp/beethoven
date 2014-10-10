from beethoven.settings_base import *

if PRODUCTION:
    from beethoven.settings_production import *
else:
    from beethoven.settings_dev import *
