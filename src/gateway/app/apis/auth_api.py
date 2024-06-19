
from flask import Blueprint, request

from ..helper.custom_response import CustomResponse
from ..services.auth_svc import access

gateway_auth_blueprint = Blueprint(
    'auth', __name__)


@gateway_auth_blueprint.route("/login", methods=["POST"])
def login():
    data, message, success, status = access.login(request)

    return CustomResponse(succeeded=success, message=message, status=status, data=data)


@gateway_auth_blueprint.route("/register", methods=["POST"])
def register():
    data, message, success, status = access.register(request)

    return CustomResponse(succeeded=success, message=message, status=status, data=data)
