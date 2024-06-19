from ..bl.storyboard_bl import get_all_projects
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
        return CustomResponse(succeeded=True, data=data, message='', status=200)
    else:
        message = result['message']
        return CustomResponse(succeeded=True, data={}, message=message, status=200)


# @storyboard_blueprint.route('/get_project/<uuid:project_id>', methods=['GET'])
# @token_required
# def get_project(current_user, project_id):
#     result = get_project_by_id(current_user['id'], project_id)
#     if result['status'] == 200:
#         return CustomResponse(succeeded=True, data=result['data'], status=200)
#     else:
#         return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


# @storyboard_blueprint.route('/create_project', methods=['POST'])
# @token_required
# def create_project(current_user):
#     data = request.get_json()
#     result = create_project_bl(data, current_user['id'])
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/script_styles', methods=['GET'])
# @token_required
# def script_styles(current_user):
#     result = get_all_script_styles()
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/storyboard_styles', methods=['GET'])
# @token_required
# def storyboard_styles(current_user):
#     result = get_all_storyboard_styles()
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/video_durations', methods=['GET'])
# @token_required
# def video_durations(current_user):
#     result = get_all_video_durations()
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/aspect_ratios', methods=['GET'])
# @token_required
# def aspect_ratios(current_user):
#     result = get_all_aspect_ratios()
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/boards_per_mins', methods=['GET'])
# @token_required
# def boards_per_mins(current_user):
#     result = get_all_boards_per_mins()
#     data = result['data']
#     return CustomResponse(succeeded=True, data=data, status=200)


# @storyboard_blueprint.route('/get_project_storyboard/<uuid:project_id>', methods=['GET'])
# @token_required
# def get_project_storyboard(current_user, project_id):
#     result = get_project_storyboard_bl(current_user['id'], project_id)
#     if result['status'] == 200:
#         return CustomResponse(succeeded=True, data=result['data'], status=200)
#     else:
#         return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


# @storyboard_blueprint.route('/get_script/<uuid:project_id>', methods=['Post'])
# @token_required
# def get_script(current_user, project_id):
#     result = send_synopsis(current_user['id'], project_id)
#     if result['status'] == 200:
#         return CustomResponse(succeeded=True, data=result['data'], status=200)
#     else:
#         return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


# @storyboard_blueprint.route('/generate_storyboards/<uuid:project_id>', methods=['Post'])
# @token_required
# def generate_storyboards(current_user, project_id):
#     result = send_script(current_user['id'], project_id)
#     if result['status'] == 200:
#         return CustomResponse(succeeded=True, data=result['data'], status=200)
#     else:
#         return CustomResponse(succeeded=False, message=result['message'], status=result['status'])
