# ============================================================================
# This is the WSGI configuration file for PythonAnywhere
# Replace the Django section in your PythonAnywhere WSGI file with this code
# Location: Web tab → WSGI configuration file
# ============================================================================

import os
import sys

# Add project directory to path
path = '/home/SAYEDALI/movie_rating_system'
if path not in sys.path:
    sys.path.append(path)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'imdb.settings'

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
