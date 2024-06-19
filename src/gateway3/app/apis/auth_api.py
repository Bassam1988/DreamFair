from flask import request

from auth_svc import access

from apis import gateway_blueprint


@gateway_blueprint.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@gateway_blueprint.route("/register", methods=["POST"])
def register():
    token, err = access.register(request)

    if not err:
        return token
    else:
        return err
