from nameko.rpc import rpc
from nameko.messaging import consume
from kombu import Queue
from t_i_service.nameko_config import TextImageServiceConfig
from app.database import init_consumer_db


class TextImageService(TextImageServiceConfig):
    name = "data_service"

    @rpc
    def get_config(self):
        # This will return the entire configuration dictionary including dynamic parts
        return self.config.get_dependency(None)

    @consume(queue=Queue(name="my_queue", durable=True, exchange_type='direct', routing_key='my_routing_key'))
    def process_message(self, body):
        with init_consumer_db() as session:
            new_record = MyModel(data=body)
            session.add(new_record)
            print(f"Saved: {body}")
