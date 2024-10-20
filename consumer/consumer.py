import pika, sys, os
import time

def start_consumer():
    # Cambia 'localhost' por 'rabbitmq', que es el nombre del servicio en Docker Compose amqp://guest:guest@localhost:5672/%2f?heartbeat=2400
    while True:
        try:
            credentials = pika.PlainCredentials('user', 'password')
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
            break  # Sale del bucle si la conexión es exitosa
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ is not available, retrying in 5 seconds...")
            time.sleep(5)
    channel = connection.channel()

    # Declara la cola
    channel.queue_declare(queue='enrollment_notifications')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Configura el consumidor
    channel.basic_consume(queue='enrollment_notifications', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

start_consumer()
        