# test_client.py
import socketio

# Initialize a Socket.IO client
sio = socketio.Client()

# Connect to the Socket.IO server
sio.connect('https://dreamfair.co/socket.io/')

# Handle the connection
@sio.event
def connect():
    print("Connected to server")
    
    # Emit a test event with acknowledgment
    sio.emit('project_status_updated', {'project_id': 123}, callback=on_ack)

# Handle disconnection
@sio.event
def disconnect():
    print("Disconnected from server")

# Define callback for server acknowledgment
def on_ack(data):
    print("Server acknowledgment:", data)
    sio.disconnect()

# Keep the connection open
sio.wait()
