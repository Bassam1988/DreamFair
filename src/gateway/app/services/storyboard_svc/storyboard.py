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
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_storyboard_user_project_by_id(request, project_id):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/get_project/{str(project_id)}",
        headers={"Authorization": token}

    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def sb_create_project(request, data):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.post(
        f"{main_url}/storyboard/create_project",
        headers={"Authorization": token},
        json=data
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def sb_update_project(request, project_id, data):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.put(
        f"{main_url}/storyboard/update_project/{str(project_id)}",
        headers={"Authorization": token},
        json=data
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_script_styles(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/script_styles",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_storyboard_styles(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/storyboard_styles",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_video_durations(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/video_durations",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_aspect_ratios(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/aspect_ratios",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_boards_per_mins(request):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/boards_per_mins",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def get_project_storyboard(request, project_id):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.get(
        f"{main_url}/storyboard/get_project_storyboard/{project_id}",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def send_synopsis_request(request, project_id, source):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.post(
        f"{main_url}/storyboard/get_script/{project_id}/{source}",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code


def send_script_request(request, project_id):
    token = request.headers.get('Authorization')

    if not token:
        raise Exception('missing credentails!')

    response = requests.post(
        f"{main_url}/storyboard/generate_storyboards/{project_id}",
        headers={"Authorization": token}
    )
    response_result = response.json()
    return response_result['data'], response_result['message'], response_result['succeeded'], response.status_code
