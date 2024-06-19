import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main_url = os.getenv('AUTH_SVC_ADDRESS')


def login(request):
    auth = request.json
    if not auth:
        return None, ("missing credentials", 401)

    # basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"{main_url}/auth/login",
        json=auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def register(request):
    data = request.json
    if not data:
        return None, ("This data is required", 401)

    response = requests.post(
        f"{main_url}/auth/register",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
