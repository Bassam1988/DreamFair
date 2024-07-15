from gevent.pywsgi import WSGIServer
from gevent.ssl import SSLContext, PROTOCOL_TLS_SERVER

from app import create_app

app = create_app()
ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('cert.pem', 'key.pem')

if __name__ == '__main__':
    # app.run(ssl_context=('cert.pem', 'key.pem'), port=5013)
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
