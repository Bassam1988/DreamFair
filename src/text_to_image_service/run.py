from app.bl.text2image_bl import consumer_bl
import sys
import os
from multiprocessing import Process

from app import create_app
from app.bl.text2image_bl import consumer_bl
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
        app.run(ssl_context=('cert.pem', 'key.pem'), port=5012)
    except KeyboardInterrupt:
        print("Flask app interrupted")


# if __name__ == '__main__':
#     print("in main")
#     consumer_process = Process(target=run_consumer)
#     consumer_process.start()

#     # Run the Flask app in the main thread
#     try:
#         run_app()
#     except KeyboardInterrupt:
#         print("Interrupted")
#         consumer_process.terminate()
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)


if __name__ == '__main__':

    run_app()


# if __name__ == '__main__':
#     print("In main - starting Flask app.")
#     flask_process = Process(target=run_app)
#     flask_process.start()

#     print("Starting consumer process.")
#     consumer_process = Process(target=run_consumer)
#     consumer_process.start()

#     flask_process.join()  # This waits for the Flask process to finish
#     consumer_process.join()
