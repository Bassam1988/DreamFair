from ..bl.storyboard_bl import create_project_bl, delete_project_by_id, delete_project_history_by_id, generate_storyboard_description, get_all_aspect_ratios, get_all_boards_per_mins, get_all_project_histories, \
    get_all_projects, get_all_script_styles, get_all_storyboard_styles, get_all_video_durations, \
    get_project_by_id, get_project_h_by_id, get_project_storyboard_bl, send_script, update_project_by_id, update_regenerate_storyboard
from ..bl.auth_svc.validate import token_required_bl
from ..helper.custom_response import CustomResponse


from flask import Blueprint, request

from functools import wraps


storyboard_blueprint = Blueprint('storyboard', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return CustomResponse(succeeded=False, message='missing credentails!', status=401)

        result = token_required_bl(token)
        status = result['status']
        if status == 200:
            current_user = result['current_user']
            return f(current_user, *args, **kwargs)
        else:
            return CustomResponse(succeeded=False, message=result['message'], status=status)

    return decorated


@storyboard_blueprint.route('/projects', methods=['GET'])
@token_required
def projects(current_user):
    result = get_all_projects(current_user['id'])
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/get_project/<uuid:project_id>', methods=['GET'])
@token_required
def get_project(current_user, project_id):
    result = get_project_by_id(current_user['id'], project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/delete_project/<uuid:project_id>', methods=['DELETE'])
@token_required
def delete_project(current_user, project_id):
    result = delete_project_by_id(current_user['id'], project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/delete_project_history/<uuid:project_h_id>', methods=['DELETE'])
@token_required
def delete_project_h(current_user, project_h_id):
    result = delete_project_history_by_id(current_user['id'], project_h_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/update_project/<uuid:project_id>', methods=['PUT'])
@token_required
def update_project(current_user, project_id):
    data = request.get_json()
    result = update_project_by_id(current_user['id'], project_id, data)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/create_project', methods=['POST'])
@token_required
def create_project(current_user):
    data = request.get_json()
    result = create_project_bl(data, current_user['id'])
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/script_styles', methods=['GET'])
@token_required
def script_styles(current_user):
    result = get_all_script_styles()
    data = result['data']
    message = result['message']
    return CustomResponse(succeeded=True, data=data, message=message, status=200)


@storyboard_blueprint.route('/storyboard_styles', methods=['GET'])
@token_required
def storyboard_styles(current_user):
    result = get_all_storyboard_styles()
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/video_durations', methods=['GET'])
@token_required
def video_durations(current_user):
    result = get_all_video_durations()
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/aspect_ratios', methods=['GET'])
@token_required
def aspect_ratios(current_user):
    result = get_all_aspect_ratios()
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/boards_per_mins', methods=['GET'])
@token_required
def boards_per_mins(current_user):
    result = get_all_boards_per_mins()
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/get_project_storyboard/<uuid:project_id>', methods=['GET'])
@token_required
def get_project_storyboard(current_user, project_id):
    result = get_project_storyboard_bl(current_user['id'], project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/get_script/<uuid:project_id>/<int:source>', methods=['Post'])
@token_required
def get_script(current_user, project_id, source):
    result = generate_storyboard_description(
        current_user['id'], project_id, source)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/generate_storyboards/<uuid:project_id>', methods=['Post'])
@token_required
def generate_storyboards(current_user, project_id):
    result = send_script(current_user['id'], project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/regenerate_storyboard/<uuid:storyboard_id>', methods=['Post'])
@token_required
def regenerate_storyboard(current_user, storyboard_id):
    req_data = request.get_json()
    scene_description = req_data['scene_description']
    result = update_regenerate_storyboard(
        current_user['id'], storyboard_id, scene_description)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@storyboard_blueprint.route('/project_histories/<uuid:project_id>', methods=['GET'])
@token_required
def project_histories(current_user, project_id):
    result = get_all_project_histories(current_user['id'], project_id)
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


@storyboard_blueprint.route('/get_project_history/<uuid:project_h_id>', methods=['GET'])
@token_required
def get_project_history(current_user, project_h_id):
    result = get_project_h_by_id(current_user['id'], project_h_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])
