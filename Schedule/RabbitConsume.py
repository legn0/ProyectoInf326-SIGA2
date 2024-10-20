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

def consume_event(cola,callback):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
                print(f"Error processing message: {e}")
                channel.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=on_message)

        print(f"[*] Esperando mensajes en {cola}.")
        channel.start_consuming()
    except Exception as e:
        print(f"Error al consumir evento {e}")

def process_event_cursos(body, routing_key):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        event = json.loads(body.decode("utf-8"))
        routing = routing_key.split(".")
        tipo = routing[0]
        id = int(routing[1])
        accion = routing[2]
        print(f"Recibido evento: {event} con routing key {routing_key}")


        if tipo == "course":
            # Verificar si el curso existe
            query = "SELECT * FROM horarios.horarios WHERE course_id = %s"
            values = (id,)
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row is None and accion != "created":
                print(f"Error: Curso con id {id} no existe")
                return
            if row is not None and accion == "created":
                print(f"Error: Curso con id {id} ya existe")
                return
            #Crea curso
            if accion == "created":
                query = "INSERT INTO horarios.horarios (course_id, created_at) VALUES (%s, CURRENT_TIMESTAMP)"
                values = (id,)
                cursor.execute(query, values)
                conn.commit()
                print("Curso creado")
            #Falta id de paralelo que debe cambiar en el body del mensaje enviado por courses por lo que no es funcional
            elif accion == "updated":
                query = "UPDATE horarios.horarios SET course_id = %s, updated_at = CURRENT_TIMESTAMP WHERE course_id = %s"
                values = (id, id)
                cursor.execute(query, values)
                conn.commit()
                print("Curso actualizado")
            #Borra todos las filas que coincidan con el id del curso
            elif accion == "deleted":
                query = "DELETE FROM horarios.horarios WHERE course_id = %s"
                values = (id,)
                cursor.execute(query, values)
                conn.commit()
                print("Curso eliminado")

        if tipo == "parallel":
            curso_id = event.get("curso",{}).get("id")
            query = "SELECT * FROM horarios.horarios WHERE parallel_id = %s"
            values = (id,)
            cursor.execute(query, values)
            row = cursor.fetchone()
            # Verificar si el paralelo existe
            if row is None and accion != "created":
                print(f"Error: Paralelo con id {id} no existe")
                return
            if row is not None and accion == "created":
                print(f"Error: Paralelo con id {id} ya existe")
                return
            #Crear paralelo a partir de curso existente
            if accion == "created":
                print(f"Creando paralelo")
                query = "UPDATE horarios.horarios SET parallel_id = %s, updated_at = CURRENT_TIMESTAMP WHERE course_id = %s"
                values = (id, curso_id)
                cursor.execute(query, values)
                conn.commit()
                print("Paralelo creado")
            #Borrar toda la fila o solo el parallel_id??
            elif accion == "deleted":
                query = "DELETE FROM horarios.horarios WHERE parallel_id = %s AND course_id = %s"
                values = (id, curso_id)
                cursor.execute(query, values)
                conn.commit()
                print("Paralelo eliminado")

    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"Error processing event: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


##Procesa los eventos de profesores, como aqui no estan vinculados con cursos o paralelos, solo se podrian eliminar de la tabla.
def process_event_users(body, routing_key):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        event = json.loads(body)
        routing = routing_key.split(".")
        tipo = routing[0]
        id = int(routing[1])
        accion = routing[2]
        print(f"Recibido evento: {event} con routing key {routing_key}")
        query = "SELECT * FROM horarios.horarios WHERE profesor_id = %s"
        values = (id,)
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row is None and accion == "deleted":
            print(f"Error: Profesor con id {id} no existe")
            return
        
        elif accion == "deleted":
            query = "UPDATE horarios.horarios SET profesor_id = NULL, nombre_profesor = NULL, updated_at = CURRENT_TIMESTAMP WHERE profesor_id = %s;"
            values = (id,)
            cursor.execute(query, values)
            conn.commit()
            print(f"Profesor con id {id} eliminado")

        print(f"Recibido evento: {event} con routing key {routing_key}")
    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"Error processing event: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def signal_handler(sig, frame):
    print('Stopping threads...')
    sys.exit(0)

#Usa threading para poder consumir ambos eventos al mismo tiempo
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    thread_cursos = threading.Thread(target=consume_event, args=("courses", process_event_cursos))
    thread_users = threading.Thread(target=consume_event, args=("users", process_event_users))

    thread_cursos.start()
    thread_users.start()

    thread_cursos.join()
    thread_users.join()

