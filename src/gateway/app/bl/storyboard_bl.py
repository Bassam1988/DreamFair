import json
from dotenv import load_dotenv
import os

from ..services.storyboard_svc.storyboard import delete_storyboard_user_project_by_id, get_aspect_ratios, get_boards_per_mins, get_project_storyboard, get_script_styles, get_storyboard_styles, get_storyboard_user_project, \
    get_storyboard_user_project_by_id, get_video_durations, sb_create_project, sb_update_project, send_script_request, send_synopsis_request, send_update_regenerate_storyboard_request

# Load environment variables from .env file
load_dotenv()


def get_all_projects(request):
    data, message, succeeded, status = get_storyboard_user_project(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_project_by_id(request, project_id):
    data, message, succeeded, status = get_storyboard_user_project_by_id(
        request, project_id)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}
    
def delete_project_by_id(request, project_id):
    data, message, succeeded, status = delete_storyboard_user_project_by_id(
        request, project_id)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def update_project_bl(request, project_id):
    data = request.json
    if not data:
        return None, ("This data is required", 401)

    data, message, succeeded, status = sb_update_project(
        request, project_id, data)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def create_project_bl(request):
    data = request.json
    if not data:
        return None, ("This data is required", 401)

    data, message, succeeded, status = sb_create_project(request, data)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_all_script_styles(request):
    data, message, succeeded, status = get_script_styles(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_all_storyboard_styles(request):
    data, message, succeeded, status = get_storyboard_styles(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_all_video_durations(request):
    data, message, succeeded, status = get_video_durations(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_all_aspect_ratios(request):
    data, message, succeeded, status = get_aspect_ratios(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_all_boards_per_mins(request):
    data, message, succeeded, status = get_boards_per_mins(request)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def get_project_storyboard_bl(request, project_id):
    data, message, succeeded, status = get_project_storyboard(
        request, project_id)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def send_synopsis(request, project_id, source):
    data, message, succeeded, status = send_synopsis_request(
        request, project_id, source)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def send_script(request, project_id):
    data, message, succeeded, status = send_script_request(
        request, project_id)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}


def update_regenerate_storyboard(request, storyboard_id):
    data = request.json
    if not data:
        return None, ("This data is required", 401)
    data, message, succeeded, status = send_update_regenerate_storyboard_request(
        request, storyboard_id,data)
    if succeeded:
        return {'data': data, 'message': message, 'status': status}
    else:
        return {'data': {}, 'message': message, 'status': status}