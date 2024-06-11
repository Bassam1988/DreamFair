import json
from nameko.rpc import rpc
from nameko.messaging import consume
from kombu import Queue
from t_i_service.nameko_config import TextImageServiceConfig
from app.database import init_consumer_db
from app.bl.text2image_bl import create_storyboard_operation_images


class TextImageService(TextImageServiceConfig):
    name = "data_service"

    @rpc
    def get_config(self):
        # This will return the entire configuration dictionary including dynamic parts
        return self.config.get_dependency(None)

    @consume(queue=Queue(name="my_queue", durable=True, exchange_type='direct', routing_key='my_routing_key'))
    def process_message(self, body):
        data = json.loads(body.decode('utf-8'))
        with init_consumer_db() as session:
            try:
                images_data = []
                reference = data['reference']
                orginal_script = data['orginal_script']
                create_storyboard_operation_images(
                    images_data, reference, orginal_script)

                print(f"Saved: {body}")
            except Exception as e:
                session.rollback()
