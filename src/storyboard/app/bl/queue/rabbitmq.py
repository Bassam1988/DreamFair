import pika
import json


class RabbitMQ():
    queues = {}

    def __init__(self, host, port, user, password, queue_name) -> None:
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.username = user
        self.password = password
        self.init_connection()

    def init_connection(self):
        """Initializes or reinitializes the connection and ensures the queue exists."""
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                heartbeat=600,  # Heartbeat timeout in seconds
                blocked_connection_timeout=300,
                virtual_host='/',
                credentials=credentials
            ))
        self.queues[self.queue_name] = connection
        channel = self.queues[self.queue_name].channel()
        channel.queue_declare(queue=self.queue_name, durable=True)

    def re_init_connection(self, retries=0):
        retries += 1
        try:
            self.init_connection()
        except Exception as e:
            if retries < 3:
                self.re_init_connection(retries)
            else:
                print("error re_init_connection: "+str(e))
                raise e

    def send_message(self, routing_key, message, retries=0):
        retries += 1
        try:
            channel = self.queues[self.queue_name].channel()
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
            print("connection error1")
            self.re_init_connection()
            self.send_message(routing_key, message)
        except Exception as e:
            if retries < 3:
                print("connection error2")
                self.re_init_connection()
                self.send_message(routing_key, message, retries)
            else:
                print("error3: "+str(e))
                raise e

    def create_callback(self, process_func, db_session, socket=None):
        def callback(ch, method, properties, body):
            err = process_func(
                body, db_session, for_consumer=True, socket=socket)
            if err:
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        return callback

    def consumer(self, queue, callback):
        channel = self.queues[self.queue_name].channel()
        channel.basic_consume(
            queue=queue, on_message_callback=callback
        )
        print("Waiting for missages. To exit press CTRL+C")

        channel.start_consuming()
