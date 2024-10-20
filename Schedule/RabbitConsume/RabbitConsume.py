from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pika
import json
import threading
import os
import signal
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rabbitmq_config = {
    'host': os.getenv('RABBITMQ_HOST', 'localhost'),
    'exchange': os.getenv('RABBITMQ_EXCHANGE', 'horario_events'),
    'exchange_type': os.getenv('RABBITMQ_EXCHANGE_TYPE', 'topic')
}

db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'admin'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'horarios')
}


def consume_event(cola, callback):
    """
    Funcion consume_event

    Consume eventos de una cola de RabbitMQ y llama a una funcion de callback para procesar el evento.

    Args:
        cola (str): Nombre de la cola a consumir
        callback (function): Funcion a llamar para procesar el evento

    Returns:
        None
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_config['host']))
        channel = connection.channel()
        channel.exchange_declare(exchange=cola, exchange_type=rabbitmq_config['exchange_type'])
        result = channel.queue_declare(queue=cola, durable=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=cola, queue=queue_name, routing_key="*.*.*")

        def on_message(channel, method, properties, body):
            try:
                callback(body, routing_key=method.routing_key)
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                channel.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=on_message)

        logger.info(f"Consumiendo eventos de la cola {cola}")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Error iniciando consumer: {e}")


def process_event_cursos(body, routing_key):
    """
    Funcion process_event_cursos

    Procesa eventos de cursos y paralelos de la cola Courses de RabbitMQ.

    Args:
        body (str): Cuerpo del mensaje
        routing_key (str): Routing key del mensaje

    Returns:
        None
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        event = json.loads(body.decode("utf-8"))
        routing = routing_key.split(".")
        tipo = routing[0]
        id = int(routing[1])
        accion = routing[2]
        logger.info(f"Recibido evento: {event} con routing key {routing_key}")

        if tipo == "course":
            # Verificar si el curso existe
            query = "SELECT * FROM horarios.horarios WHERE course_id = %s"
            values = (id,)
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row is None and accion != "created":
                logger.error(f"Error: Curso con id {id} no existe")
                return
            if row is not None and accion == "created":
                logger.error(f"Error: Curso con id {id} ya existe")
                return
            # Crea curso
            if accion == "created":
                query = "INSERT INTO horarios.horarios (course_id, created_at) VALUES (%s, CURRENT_TIMESTAMP)"
                values = (id,)
                cursor.execute(query, values)
                conn.commit()
                logger.info("Curso creado")
            # Falta id de paralelo que debe cambiar en el body del mensaje enviado por courses por lo que no es funcional
            elif accion == "updated":
                query = "UPDATE horarios.horarios SET course_id = %s, updated_at = CURRENT_TIMESTAMP WHERE course_id = %s"
                values = (id, id)
                cursor.execute(query, values)
                conn.commit()
                logger.info("Curso actualizado")
            # Borra todos las filas que coincidan con el id del curso
            elif accion == "deleted":
                query = "DELETE FROM horarios.horarios WHERE course_id = %s"
                values = (id,)
                cursor.execute(query, values)
                conn.commit()
                logger.info("Curso eliminado")

        if tipo == "parallel":
            curso_id = event.get("curso", {}).get("id")
            query = "SELECT * FROM horarios.horarios WHERE parallel_id = %s"
            values = (id,)
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Verificar si el paralelo existe
            if row is None and accion != "created":
                logger.error(f"Error: Paralelo con id {id} no existe")
                return
            if row is not None and accion == "created":
                logger.error(f"Error: Paralelo con id {id} ya existe")
                return
            # Crear paralelo a partir de curso existente
            if accion == "created":
                logger.info(f"Creando paralelo")
                query = "UPDATE horarios.horarios SET parallel_id = %s, updated_at = CURRENT_TIMESTAMP WHERE course_id = %s"
                values = (id, curso_id)
                cursor.execute(query, values)
                conn.commit()
                logger.info("Paralelo creado")
            # Borra paralelo y sus datos asociados
            elif accion == "deleted":
                query = "UPDATE horarios.horarios SET parallel_id = NULL, id_profesor = NULL, nombre_profesor = NULL, bloque_id = NULL, tipo = NULL,  updated_at = CURRENT_TIMESTAMP WHERE parallel_id = %s"
                values = (id, curso_id)
                cursor.execute(query, values)
                conn.commit()
                logger.info("Paralelo eliminado")

    except mysql.connector.Error as db_err:
        logger.error(f"Database error: {db_err}")
    except Exception as e:
        logger.error(f"Error processing event: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def process_event_users(body, routing_key):
    """
    Funcion process_event_users

    Procesa eventos de profesores de la cola Users de RabbitMQ.

    Args:
        body (str): Cuerpo del mensaje
        routing_key (str): Routing key del mensaje

    Returns:
        None
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        event = json.loads(body)
        routing = routing_key.split(".")
        tipo = routing[0]
        id = int(routing[1])
        accion = routing[2]
        logger.info(f"Recibido evento: {event} con routing key {routing_key}")
        query = "SELECT * FROM horarios.horarios WHERE id_profesor = %s"
        values = (id,)
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row is None and accion == "deleted":
            logger.error(f"Error: Profesor con id {id} no existe")
            return

        elif accion == "deleted":
            query = "UPDATE horarios.horarios SET id_profesor = NULL, nombre_profesor = NULL, updated_at = CURRENT_TIMESTAMP WHERE id_profesor = %s;"
            values = (id,)
            cursor.execute(query, values)
            conn.commit()
            logger.info(f"Profesor con id {id} eliminado")

        logger.info(f"Recibido evento: {event} con routing key {routing_key}")
    except mysql.connector.Error as db_err:
        logger.error(f"Database error: {db_err}")
    except Exception as e:
        logger.error(f"Error processing event: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def signal_handler(sig, frame):
    logger.info('Stopping threads...')
    sys.exit(0)


# Usa threading para poder consumir ambos eventos al mismo tiempo
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    thread_cursos = threading.Thread(target=consume_event, args=("courses", process_event_cursos))
    thread_users = threading.Thread(target=consume_event, args=("users", process_event_users))

    thread_cursos.start()
    thread_users.start()

    thread_cursos.join()
    thread_users.join()