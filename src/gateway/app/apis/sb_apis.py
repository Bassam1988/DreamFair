from ..bl.storyboard_bl import delete_project_by_id, delete_project_h_by_id, get_all_aspect_ratios, get_all_boards_per_mins, get_all_project_history, get_all_projects, get_all_script_styles, get_all_storyboard_styles, get_all_video_durations, get_project_by_id, create_project_bl, get_project_h_by_id, get_project_storyboard_bl, send_script, send_synopsis, update_project_bl, update_regenerate_storyboard
from ..helper.custom_response import CustomResponse


from flask import Blueprint, request

gateway_sb_blueprint = Blueprint(
    'storyboard', __name__)


@gateway_sb_blueprint.route('/projects', methods=['GET'])
def projects():
    result = get_all_projects(request)
    status = result['status']
    if status == 200:
        data = result['data']
        return CustomResponse(succeeded=True, data=data, message='', status=status)
    else:
        message = result['message']
        return CustomResponse(succeeded=True, data={}, message=message, status=status)


@gateway_sb_blueprint.route('/get_project/<uuid:project_id>', methods=['GET'])
def get_project(project_id):
    result = get_project_by_id(request, project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/project_histories/<uuid:project_id>', methods=['GET'])
def project_histories(project_id):
    result = get_all_project_history(request, project_id)
    status = result['status']
    if status == 200:
        data = result['data']
        return CustomResponse(succeeded=True, data=data, message='', status=status)
    else:
        message = result['message']
        return CustomResponse(succeeded=True, data={}, message=message, status=status)


@gateway_sb_blueprint.route('/get_project_history/<uuid:project_h_id>', methods=['GET'])
def get_project_h(project_h_id):
    result = get_project_h_by_id(request, project_h_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/delete_project/<uuid:project_id>', methods=['DELETE'])
def delete_project(project_id):
    result = delete_project_by_id(request, project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/delete_project_history/<uuid:project_id>', methods=['DELETE'])
def delete_project_h(project_id):
    result = delete_project_h_by_id(request, project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/update_project/<uuid:project_id>', methods=['PUT'])
def update_project(project_id):
    result = update_project_bl(request, project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/create_project', methods=['POST'])
def create_project():
    result = create_project_bl(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/script_styles', methods=['GET'])
def script_styles():
    result = get_all_script_styles(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/storyboard_styles', methods=['GET'])
def storyboard_styles():
    result = get_all_storyboard_styles(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/video_durations', methods=['GET'])
def video_durations():
    result = get_all_video_durations(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/aspect_ratios', methods=['GET'])
def aspect_ratios():
    result = get_all_aspect_ratios(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/boards_per_mins', methods=['GET'])
def boards_per_mins():
    result = get_all_boards_per_mins(request)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/get_project_storyboard/<uuid:project_id>', methods=['GET'])
def get_project_storyboard(project_id):
    result = get_project_storyboard_bl(request, project_id)
    data = result['data']
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=data, status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/get_script/<uuid:project_id>/<int:source>', methods=['Post'])
def get_script(project_id, source):
    result = send_synopsis(request, project_id, source)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/generate_storyboards/<uuid:project_id>', methods=['Post'])
def generate_storyboards(project_id):
    result = send_script(request, project_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@gateway_sb_blueprint.route('/regenerate_storyboard/<uuid:storyboard_id>', methods=['Post'])
def regenerate_storyboard(storyboard_id):
    result = update_regenerate_storyboard(request, storyboard_id)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, data=result['data'], status=200)
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])
