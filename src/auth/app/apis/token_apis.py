from ..helper.custom_response import CustomResponse
from ..apis.apis import token_required
from ..helper.token_helper_functions import generate_access_token
from ..schemas.schemas import UserSchema
from flask import current_app
from flask import Blueprint, request, jsonify
import jwt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token_blueprint = Blueprint('token', __name__)


@token_blueprint.route('/refresh', methods=['POST'])
def refresh_access_token():
    refresh_token = request.headers.get('x-refresh-token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 401

    try:
        data = jwt.decode(
            refresh_token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        if data['type'] == 'refresh':
            new_access_token = generate_access_token(data['user_id'])
            return jsonify({'access_token': new_access_token})
        else:
            return jsonify({'message': 'Invalid refresh token'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@token_blueprint.route('/validate', methods=['GET'])
@token_required
def validate(current_user):
    user_schema = UserSchema()
    data = {
        'user': user_schema.dump(current_user)
    }
    return CustomResponse(succeeded=True, data=data, status=200)
