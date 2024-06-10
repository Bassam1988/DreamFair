import requests
import json
from flask import current_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def token_required_bl(token):

    response = requests.get(
        f"{os.getenv('AUTH_SVC_ADDRESS')}/token/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        response_data = json.loads(response.text)
        user_data = response_data.get('data', {}).get('user', {})
        return {'current_user': user_data, 'message': '', 'status': 200}
    else:
        return {'message': response.text, 'status': response.status_code}
