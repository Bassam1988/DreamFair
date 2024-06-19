
from flask import Blueprint, request
from ..services.auth_svc import access

gateway_auth_blueprint = Blueprint(
    'auth', __name__)


@gateway_auth_blueprint.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@gateway_auth_blueprint.route("/register", methods=["POST"])
def register():
    token, err = access.register(request)

    if not err:
        return token
    else:
        return err
