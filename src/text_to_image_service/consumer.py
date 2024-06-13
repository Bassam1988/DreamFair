import sys
import os

from app.bl import text2image_bl
from app.database import init_consumer_db


if __name__ == "__main__":
    db_session = init_consumer_db()
    try:
        print("run_consumer")
        # Assuming this is a blocking function that runs indefinitely
        text2image_bl.consumer_bl(db_session)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        db_session.remove()
