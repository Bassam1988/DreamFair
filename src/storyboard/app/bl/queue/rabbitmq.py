import pika
import json


class RabbitMQ():
    queues = {}

    def __init__(self, host, port, user, password, queue_name) -> None:
        self.host = host
        self.port = port
        self.queue_name = queue_name
        if self.queue_name in self.queues:
            return
        credentials = pika.PlainCredentials(user, password)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                heartbeat=600,  # Heartbeat timeout in seconds
                blocked_connection_timeout=300,
                virtual_host='/',
                credentials=credentials
            ))
        self.queues[queue_name] = connection

    def re_init_connection(self):
        host = self.host
        port = self.port
        q_name = self.queue_name
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                heartbeat=600,  # Heartbeat timeout in seconds
                blocked_connection_timeout=300,
                virtual_host='/'
            ))
        self.queues[q_name] = connection

    def send_message(self, routing_key, message):
        try:
            channel = self.queues[self.q_name].channel()
            channel.queue_declare(queue=routing_key, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
        # ConnectionClosed:#StreamLostError
        except pika.exceptions.ConnectionWrongStateError:
            self.re_init_connection()
            channel = self.queues[self.q_name].channel()
            channel.queue_declare(queue=routing_key, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )

    def create_callback(self, process_func, db_session):
        def callback(ch, method, properties, body):
            err = process_func(body, db_session, for_consumer=True)
            if err:
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        return callback

    def consumer(self, queue, callback):
        channel = self.queues[self.q_name].channel()
        channel.basic_consume(
            queue=queue, on_message_callback=callback
        )
        print("Waiting for missages. To exit press CTRL+C")

        channel.start_consuming()
