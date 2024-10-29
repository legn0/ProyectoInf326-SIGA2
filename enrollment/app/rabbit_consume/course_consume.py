import pika
import json
from app.crud.crud import EnrollmentCRUD
from app.database.database import SessionLocal

def delete_course_records(course_id):
    """
    Elimina los registros del curso en la base de datos.
    """
    db = SessionLocal() 
    try:
        crud = EnrollmentCRUD(db)
        crud.delete_course(course_id)
        print(f"Curso con ID {course_id} eliminado correctamente.")
    except Exception as e:
        print(f"Error eliminando el curso con ID {course_id}: {e}")
    finally:
        db.close()

def delete_parallel_records(parallel_id):
    """
    Elimina los registros del curso en la base de datos.
    """
    db = SessionLocal() 
    try:
        crud = EnrollmentCRUD(db)
        crud.delete_parallel(parallel_id)
        print(f"Curso con ID {parallel_id} eliminado correctamente.")
    except Exception as e:
        print(f"Error eliminando el curso con ID {parallel_id}: {e}")
    finally:
        db.close()

def on_message(channel, method, properties, body):
    """
    Callback para consumir mensajes de RabbitMQ.
    """
    try:
        message = json.loads(body)
        print(f"Mensaje recibido: {message}")

        # Extraer el course_id del routing key (e.g., "course.123.deleted")
        routing_key = method.routing_key.split('.')
        entity = routing_key[0]
        entity_id = int(routing_key[1])

        # Llama a la función de eliminación correspondiente
        if entity == "course":
            delete_course_records(entity_id)
        elif entity == "parallel":
            delete_parallel_records(entity_id)
        else:
            print(f"Clave de enrutamiento desconocida: {entity}")
        
        # Acknowledge el mensaje
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Mensaje procesado para {routing_key[0]}: {id}")

    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag)

def consume_rabbitmq_messages():
    """
    Se conecta a RabbitMQ y consume mensajes de 'course.*.deleted'.
    """
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters("amqp://guest:guest@rabbitmq:5672/%2f?heartbeat=600")
        )
        channel = connection.channel()

        # Declarar el intercambio 'courses' (debe coincidir con el productor)
        channel.exchange_declare(
            exchange='courses',
            exchange_type='topic',
            durable=False  # Asegúrate de que coincida con el intercambio existente
        )

        # Declarar la cola y vincularla al intercambio con 'course.*.deleted'
        queue = channel.queue_declare(queue='enrollment_queue', durable=True)
        queue_name = queue.method.queue

        channel.queue_bind(exchange='courses', queue=queue_name, routing_key='course.*.deleted')
        channel.queue_bind(exchange='courses', queue=queue_name, routing_key='parallel.*.deleted')

        print('Esperando mensajes de RabbitMQ...')

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message,
            auto_ack=False
        )

        channel.start_consuming()

    except Exception as e:
        print(f"Error en la conexión de RabbitMQ: {e}")

if __name__ == "__main__":
    consume_rabbitmq_messages()
