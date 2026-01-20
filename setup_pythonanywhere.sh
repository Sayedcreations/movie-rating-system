#!/bin/bash
# PythonAnywhere Setup Script for Movie Rating System
# Run this in PythonAnywhere Bash Console

set -e

echo "==== Movie Rating System - PythonAnywhere Setup ===="
echo ""

# Set your PythonAnywhere username
PAYUSER="SAYEDALI"
PROJECTNAME="movie_rating_system"
PROJECTDIR="/home/$PAYUSER/$PROJECTNAME"

echo "Username: $PAYUSER"
echo "Project: $PROJECTNAME"
echo "Directory: $PROJECTDIR"
echo ""

# Step 1: Clone repository
echo "[1/6] Cloning repository from GitHub..."
cd /home/$PAYUSER
if [ -d "$PROJECTNAME" ]; then
    echo "Removing existing directory..."
    rm -rf "$PROJECTNAME"
fi
git clone https://github.com/Sayedcreations/movie-rating-system.git $PROJECTNAME
cd $PROJECTDIR

# Step 2: Create virtual environment
echo "[2/6] Creating virtual environment..."
mkvirtualenv --python=/usr/bin/python3.10 $PROJECTNAME

# Step 3: Install dependencies
echo "[3/6] Installing dependencies..."
pip install -r requirements.txt

# Step 4: Run migrations
echo "[4/6] Running database migrations..."
python manage.py migrate

# Step 5: Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput

# Step 6: Create superuser
echo "[6/6] Creating superuser account..."
echo ""
echo "Enter superuser details:"
python manage.py createsuperuser

echo ""
echo "==== Setup Complete! ===="
echo ""
echo "Next steps:"
echo "1. Go to https://www.pythonanywhere.com/user/$PAYUSER/webapps/"
echo "2. Edit WSGI configuration file"
echo "3. Add static files mapping:"
echo "   URL: /static/"
echo "   Directory: $PROJECTDIR/assets"
echo "4. Click 'Reload' button"
echo ""
echo "Then visit: https://$PAYUSER.pythonanywhere.com/"
echo ""
