import sys
import os
from multiprocessing import Process

from app import create_app
from app.bl.text2text_bl import consumer_bl
from app.database import init_consumer_db

app = create_app()


def run_consumer():
    db_session = init_consumer_db()
    try:
        print("run_consumer")
        # Assuming this is a blocking function that runs indefinitely
        consumer_bl(db_session)
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        db_session.remove()


def run_app():
    try:
        app.run(ssl_context=('cert.pem', 'key.pem'), port=5011)
    except KeyboardInterrupt:
        print("Flask app interrupted")


if __name__ == '__main__':
    print("in main")
    consumer_process = Process(target=run_consumer)
    consumer_process.start()

    # Run the Flask app in the main thread
    try:
        run_app()
    except KeyboardInterrupt:
        print("Interrupted")
        consumer_process.terminate()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
