import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main_url = os.getenv('STORYBOARD_SVC_ADDRESS')


def get_storyboard_user_project(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/projects",
        headers={"Authorization": token}

    )

    # if response.status_code == 200:
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code
    # else:
    #     return None, (response.text, response.status_code)
