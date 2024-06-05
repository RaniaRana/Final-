# Final
SE-3355 Final Assignment IMDB Clone

## Overview
This application is built with Django and initially uses SQLite for development. For production environments, it has been migrated to MySQL.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

The `requirements.txt` includes essential libraries such as Django, mysqlclient, and other dependencies needed for the project to run.

### Setting Up the Database
This application supports MySQL in production. To configure MySQL:
1. Install MySQL on your server.
2. Create a database for your application.
3. Configure your Django settings to connect to your MySQL database:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_mysql_user',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
           'PORT': '3306',
       }
   }
   ```

### Running the Application
Migrate the database schemas:
```bash
python manage.py migrate
```
Start the server:
```bash
python manage.py runserver
```

## Usage
Access the application by navigating to `http://127.0.0.1:8000/` in your web browser.

## Important Notes
- Some videos within the application cannot be accessed due to copyright restrictions.
- Ensure that you use appropriate credentials and settings for the MySQL database in production.
