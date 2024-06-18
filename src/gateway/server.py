from flask import Flask, request


from auth_svc import access


server = Flask(__name__)


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/register", methods=["POST"])
def register():
    token, err = access.register(request)

    if not err:
        return token
    else:
        return err


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
