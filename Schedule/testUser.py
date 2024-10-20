import pika
import json

def publish_test_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='users', exchange_type='topic')
    
    message = {'test': 'Muere profesor'}
    channel.basic_publish(
        exchange='users',
        routing_key='professor.2.deleted',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent 'Test Message'")
    connection.close()

if __name__ == "__main__":
    publish_test_message()

    