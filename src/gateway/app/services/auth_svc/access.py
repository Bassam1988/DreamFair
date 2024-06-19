import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main_url = os.getenv('AUTH_SVC_ADDRESS')


def login(request):
    auth = request.json
    if not auth:
        return {}, "missing credentials", False, 401

    # basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"{main_url}/auth/login",
        json=auth
    )

    res_data = response.json()
    return res_data['data'], res_data['message'], res_data['succeeded'], response.status_code


def register(request):
    data = request.json
    if not data:
        return None, ("This data is required", 401)

    response = requests.post(
        f"{main_url}/auth/register",
        json=data
    )

    res_data = response.json()
    return res_data['data'], res_data['message'], res_data['succeeded'], response.status_code
