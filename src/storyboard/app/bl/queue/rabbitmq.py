import pika
import json


class rabbitmq():
    queues = {}

    def __init__(self, host) -> None:
        self.host = host
        if self.host in self.queues:
            return
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                heartbeat=600,  # Heartbeat timeout in seconds
                blocked_connection_timeout=300
            ))
        self.queues[host] = connection

    def send_message(self, routing_key, message):
        channel = self.queues[self.host].channel()
        channel.basic_publish(
            exchange="",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
