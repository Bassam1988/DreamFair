import sys
import os
from multiprocessing import Process
import socketio
from app.bl import storyboard_bl
from app.database import init_consumer_db


def run_consumer_bl(consumer_function):
    # Initialize a new Socket.IO client for this process
    sio = socketio.Client()
    sio.connect(os.getenv('SOCKETIO_SERVER_URL', 'http://localhost:5002'))
    
    db_session = init_consumer_db()  # Initialize db session inside each process
    try:
        print(f"Running {consumer_function.__name__}")
        consumer_function(db_session, sio)
    except KeyboardInterrupt:
        print(f"{consumer_function.__name__} Interrupted")
    finally:
        db_session.remove()  # Ensure db_session is closed properly
        sio.disconnect()  # Disconnect the Socket.IO client
        print(f"{consumer_function.__name__} session closed.")


if __name__ == "__main__":
    # Create a Socket.IO client
    
    # Create processes for each consumer
    process1 = Process(target=run_consumer_bl, args=(
        storyboard_bl.t2t_consumer_bl,))
    process2 = Process(target=run_consumer_bl, args=(
        storyboard_bl.t2m_consumer_bl,))

    process1.start()
    process2.start()

    try:
        # Wait for both processes to complete, which they never will unless interrupted
        process1.join()
        process2.join()
    except KeyboardInterrupt:
        print("Main process interrupted")
        process1.terminate()
        process2.terminate()
    finally:        
        sys.exit(0)
        
