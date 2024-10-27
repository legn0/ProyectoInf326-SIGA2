#from ..crud.crud import EnrollmentCRUD
#from ..database.database import get_db
import pika
        
#db= get_db

def delete_course_records(course_id):
    print(course_id)
    #crud = EnrollmentCRUD(db)
    #crud.delete_course(course_id)

def on_message(channel, method, properties, body):
    print("hola")
    """
    Callback function for consuming messages.
    Args:
        channel: The channel object.
        method: Delivery method.
        properties: Message properties.
        body: The message body.
    """
    """try:
        message = json.loads(body)
        # Extract course_id from routing key (e.g., "course.123.deleted")
        routing_key = method.routing_key
        course_id = int(routing_key.split('.')[1])
        
        # Call the delete function
        delete_course_records(course_id)

        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Processed message for course_id {course_id}")

    except Exception as e:
        print(f"Error processing message: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag)"""

def consume_messages():
    """
    Connects to RabbitMQ and consumes messages with the routing key 'course.*.deleted'.
    """
    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare exchange and queue (if not already created)
        channel.exchange_declare(exchange='courses', exchange_type='topic', durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the routing key pattern
        channel.queue_bind(exchange='courses', queue=queue_name, routing_key='course.*.deleted')

        print('Waiting for messages. To exit press CTRL+C')

        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        channel.start_consuming()

    except KeyboardInterrupt:
        print('Interrupted')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection is not None and connection.is_open:
            connection.close()

if __name__ == "__main__":
    consume_messages()