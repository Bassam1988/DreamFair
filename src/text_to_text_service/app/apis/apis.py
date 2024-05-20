
from ..bl.text2text_bl import generate_script
from ..bl.auth_svc.validate import token_required_bl
from ..helper.custom_response import CustomResponse


from flask import Blueprint, request

from functools import wraps


text2text_blueprint = Blueprint('text2text', __name__)


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


@text2text_blueprint.route('/create_script', methods=['POST'])
@token_required
def create_script(current_user):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    result = generate_script(data)
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)
