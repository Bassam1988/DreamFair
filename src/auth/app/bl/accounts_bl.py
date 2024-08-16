import jwt
from ..helper.token_helper_functions import generate_access_token, generate_refresh_token, generate_token
from ..models.r_token import RefreshToken
from ..models.models import Role, User
from ..schemas.schemas import UserSchema
from ..database import db_session
from flask import current_app
from sqlalchemy import and_, or_


def register_bl(data):
    user_schema = UserSchema()
    errors = user_schema.validate(data)
    if errors:
        return {'message': errors, 'status': 400}
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    if 'role_ids' in data:
        # Role.query.filter(Role.id.in_(data['role_ids'])).all()
        roles = db_session.query(Role).filter(
            Role.id.in_(data['role_ids'])).all()
        if not roles:
            return {'message': 'One or more roles are invalid', 'status': 400}
        user.roles = roles
    existed_user = db_session.query(User).filter(
        or_(User.email == data['email'], User.username == data['username'])
    ).all()
    if existed_user:
        return {'message': 'the username or email exists, please choose another', 'status': 400}
    db_session.add(user)
    db_session.commit()
    return {'data': {'user': user_schema.dump(user)}, 'safe': False, 'status': 201}


def login_bl(data):
    user = User.query.filter_by(username=data.get('username')).first()
    if not user:
        return {'message': 'Could not verify', 'status': 401}

    if user.check_password(data.get('password')):

        roles = user.roles
        roles_string = ""
        for role in roles:
            roles_string += role.name+","
        role_list = roles_string.split(",")
        user_id = user.id
        token = generate_token(user_id, roles_string)
        token_data = {
            'token': token
        }
        return {'status': 200, 'data': {'token_data': token_data}}

    return {'message': 'Could not verify', 'status': 403}


def token_required_bl(token):
    try:
        data = jwt.decode(
            token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(id=data['user_id']).first()
        if not current_user:
            return {'message': 'User not found.', 'status': 404}
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired', 'status': 401}
    except jwt.InvalidTokenError:
        return {'message': 'Token is invalid', 'status': 401}

    return {'current_user': current_user, 'message': '', 'status': 200}


def logout_bl(user):
    user_id = user.id
    # Invalidate or delete the refresh token
    RefreshToken.query.filter_by(user_id=user_id).delete()
    # db_session = db_session()
    db_session.commit()
    return {'message': '', 'status': 200}
