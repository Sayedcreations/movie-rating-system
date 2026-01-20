# PythonAnywhere Deployment Guide

## Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a FREE account
3. Verify your email

## Step 2: Set Up Your Web App

### In PythonAnywhere Dashboard:

1. Click **"Web"** in the top menu
2. Click **"Add a new web app"**
3. Choose:
   - **Domain**: your-username.pythonanywhere.com
   - **Python Framework**: Django
   - **Python Version**: 3.10 or 3.11

4. For source code location, choose: **"Clone from GitHub"**
   - Repository URL: `https://github.com/Sayedcreations/movie-rating-system.git`

## Step 3: Configure in Bash Console

Click on **"Bash Console"** and run:

```bash
cd /home/your-username/movie-rating-system

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.11 movie-venv

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Step 4: Update WSGI File

In PythonAnywhere Web tab, click on the **WSGI configuration file** link.

Replace the Django section with:

```python
import os
import sys
from pathlib import Path

path = '/home/your-username/movie-rating-system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'imdb.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 5: Configure Settings for Production

Update your Django settings for production:

In **imdb/settings.py**, modify:

```python
ALLOWED_HOSTS = ['your-username.pythonanywhere.com', 'localhost', '127.0.0.1']
DEBUG = False  # Set to False in production (or use environment variable)
```

## Step 6: Static Files

In Bash Console:
```bash
python manage.py collectstatic --noinput
```

In PythonAnywhere Web tab, add a static mapping:
- URL: `/static/`
- Directory: `/home/your-username/movie-rating-system/assets`

## Step 7: Reload & Go Live

1. Go back to **Web** tab
2. Click **"Reload your-username.pythonanywhere.com"**
3. Wait 1-2 minutes for reload
4. Visit: `https://your-username.pythonanywhere.com/`

## Step 8: Admin Access

Login at: `https://your-username.pythonanywhere.com/admin/`

Use credentials created in Step 3

---

## Troubleshooting

### Check Error Logs:
- Click **"Web"** → scroll down → **"Error log"**

### Common Issues:
1. **Static files not loading**: Recollect static files and reload
2. **404 errors**: Check WSGI configuration
3. **Database errors**: Ensure migrations were run

### Get Help:
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Docs: https://docs.djangoproject.com/

---

**Need help?** Share your PythonAnywhere username after setup for specific troubleshooting!
