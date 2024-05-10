import datetime
from ..models.r_token import RefreshToken
import jwt
from flask import current_app
from ..database import db_session


def generate_token(user_id, role):
    payload = {
        'user_id': str(user_id),  # Identifier for the user
        # Token expiration time
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),  # Token issued at time
        'role': role
    }
    token = jwt.encode(
        payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


def generate_access_token(user_id):
    payload = {
        'user_id': str(user_id),  # Identifier for the user
        # Token expiration time
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),  # Token issued at time
        'type': 'access'
    }
    token = jwt.encode(
        payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


def generate_refresh_token(user_id):
    payload = {
        'user_id': str(user_id),
        # Longer expiration time
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow(),
        'type': 'refresh'  # Optionally distinguish between token types
    }
    refresh_token = jwt.encode(
        payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return refresh_token


def issue_refresh_token(user):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=30)  # 30 days validity
    token = jwt.encode({'user_id': str(user.id), 'exp': expiry},
                       current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    # Save the token in the database
    refresh_token = RefreshToken(
        token=token, user_id=user.id, expires_at=expiry)

    db_session.add(refresh_token)
    db_session.commit()

    return token
