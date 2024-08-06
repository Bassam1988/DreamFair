from gevent.pywsgi import WSGIServer
from gevent.ssl import SSLContext, PROTOCOL_TLS_SERVER

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5013)
