from flask import current_app

import json
import requests


def token_required_bl(token):

    response = requests.get(
        f"{current_app.config.get('AUTH_SVC_ADDRESS')}/token/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        response_data = json.loads(response.text)
        user_data = response_data.get('data', {}).get('user', {})
        return {'current_user': user_data, 'message': '', 'status': 200}
    else:
        return {'message': response.text, 'status': response.status_code}

