import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main_url = {os.getenv('AUTH_SVC_ADDRESS')}


def get_storyboard_user_project(user_id):
    response = requests.get(
        f"{os.getenv('AUTH_SVC_ADDRESS')}/auth/login/{user_id}",

    )

    if response.status_code == 200:
        data = response.data
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def register(request):
    data = request.json
    if not data:
        return None, ("This data is required", 401)

    response = requests.post(
        f"{os.environ.get('AUTH_SVC_ADDRESS')}/auth/register",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
