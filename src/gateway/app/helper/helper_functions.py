from flask import request,  current_app, redirect
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def set_hsts_header(response):
    if 'https' in request.url:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


def https_redirect():
    # Check if the request is secure (HTTPS) and if the app is not in development mode
    if not request.is_secure and os.getenv('ENV') != 'development':
        # Replace 'http://' with 'https://' in the request URL
        secure_url = request.url.replace('http://', 'https://', 1)
        # Redirect to the secure URL with status code 301 (Moved Permanently)
        return redirect(secure_url, code=301)
