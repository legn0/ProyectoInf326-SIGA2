import pika
import time

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

def start_consumer():
    # Cambia 'localhost' por 'rabbitmq', que es el nombre del servicio en Docker Compose
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declara la cola
    channel.queue_declare(queue='enrollment_notifications')

    # Configura el consumidor
    channel.basic_consume(queue='enrollment_notifications', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()