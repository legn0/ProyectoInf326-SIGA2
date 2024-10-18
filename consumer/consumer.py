import pika, sys, os
import time

def start_consumer():
    # Cambia 'localhost' por 'rabbitmq', que es el nombre del servicio en Docker Compose
    connection = pika.BlockingConnection(pika.URLParameters(f"amqp://guest:guest@localhost:5672/%2f?heartbeat=2400"))
    channel = connection.channel()

    # Declara la cola
    channel.queue_declare(queue='enrollment_notifications')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Configura el consumidor
    channel.basic_consume(queue='enrollment_notifications', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)