# settings.py

INSTALLED_APPS = [
    # other apps
    'corsheaders',
    # other apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # other middleware
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Add your server's IP address or domain name if applicable
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",          # This allows requests from the root of your React app
     # This allows requests from your specific route
]

# Optional settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'content-type',
    # Add other headers as needed
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]
