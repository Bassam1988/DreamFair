from ..bl.accounts_bl import login_bl, logout_bl, register_bl, token_required_bl
from ..helper.custom_response import CustomResponse
from ..models.r_token import RefreshToken

from flask import Blueprint, request, jsonify

from functools import wraps


auth_blueprint = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        token = authorization.split(" ")[1]

        if not token:
            return CustomResponse(succeeded=False, message='Token is missing!', status=401)
        result = token_required_bl(token)
        status = result['status']
        if status == 200:
            current_user = result['current_user']
            return f(current_user, *args, **kwargs)
        else:
            return CustomResponse(succeeded=False, message=result['message'], status=status)

    return decorated


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result = register_bl(data)
    if result['status'] in (200, 201):
        return CustomResponse(succeeded=True, data=result['data'], status=result['status'], safe=result['safe'])
    else:
        return CustomResponse(succeeded=False, message=result['message'], status=result['status'])


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return CustomResponse(succeeded=False, message='Could not verify', status=401, **{'WWW-Authenticate': 'Basic realm="Login required!"'})

    result = login_bl(data)
    status = result['status']
    if status == 200:
        return CustomResponse(succeeded=True, message='', status=status, data=result['data'])
    else:
        return CustomResponse(succeeded=False, message='Could not verify', status=status, **{'WWW-Authenticate': 'Basic realm="Incorrect credential!"'})


@auth_blueprint.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    # Assuming `current_user` is the user instance obtained from the validated access token
    result = logout_bl(current_user)
    if result['status'] == 200:
        return CustomResponse(succeeded=True, message='Logged out successfully', status=200)
