# Movie Rating System

A Django-based movie rating and management system with separate portals for producers, users, and admins.

## Features

- **Producer Portal**: Add/edit movies, manage cast and crew, upload photos
- **User Portal**: Browse movies, rate movies, manage profile
- **Admin Dashboard**: Monitor system data, manage users, producers, and content
- **Movie Database**: Comprehensive movie information including cast, crew, genres, and ratings

## Tech Stack

- **Backend**: Django 6.0.1
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Django Development Server

## Installation

### Prerequisites

- Python 3.13+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/movie-rating-system.git
cd movie-rating-system
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - **Windows**:
   ```bash
   .venv\Scripts\activate
   ```
   - **macOS/Linux**:
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install django pillow
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
movie-rating-system/
├── imdb/                 # Main Django project settings
├── filim_pro/           # Producer app
├── filim_user/          # User app
├── site_admin/          # Admin app
├── index/               # Index/home app
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded media
├── manage.py            # Django management script
└── db.sqlite3           # SQLite database
```

## Usage

### Admin Portal
- Access: `http://localhost:8000/admin/`
- Login with admin credentials

### Producer Portal
- Access: `http://localhost:8000/pro/`
- Register or login as a producer
- Manage movies, cast, and crew

### User Portal
- Access: `http://localhost:8000/user/`
- Register or login as a user
- Browse and rate movies

## Default Admin Access

To create a superuser account:
```bash
python manage.py createsuperuser
```

## License

This project is created by **Sayed Alavi**
- Email: sayedalavi726@gmail.com
- Location: Dubai, UAE
- Phone: +971 54 528 1314

## Contributing

Feel free to fork this project and submit pull requests with improvements.

---

**Live URL**: `http://127.0.0.1:8000/` (Local Development)
