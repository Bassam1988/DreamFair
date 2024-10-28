# socketio_server.py
import socketio
from eventlet import wsgi
import eventlet

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Optional: Handle client connections if needed
@sio.event
def connect(sid, environ):
    print(f'Client connected: {sid}')

# Optional: Handle client disconnections
@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')

@sio.event
def project_status_updated(sid, data):
    print("Received update for project:", data)
    return {"status": "received"}  # Acknowledgment sent to the client

if __name__ == '__main__':
    # Run the server using a WSGI server like eventlet or gevent
    
    wsgi.server(eventlet.listen(('', 5002)), app)
