# socketio_server.py
import socketio
from eventlet import wsgi
import eventlet

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', 
    ping_timeout=60000,  # 60 seconds
    ping_interval=25000  # 25 seconds
    )
app = socketio.WSGIApp(sio)

# Optional: Handle client connections if needed
@sio.event
def connect(sid, environ):
    print(f'Client connected: {sid}')

# Optional: Handle client disconnections
@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')

# @sio.event
# def project_status_updated(sid, data):
#     print("Received update for project:", data)
#     return {"status": "received", "data":data}  # Acknowledgment sent to the client

@sio.event
def project_status_updated(sid, data):
    print("Received project update:", data)
    
    # Broadcast the project update to all connected clients
    sio.emit('broadcast_project_update', data)

if __name__ == '__main__':
    # Run the server using a WSGI server like eventlet or gevent
    
    wsgi.server(eventlet.listen(('', 5002)), app)
