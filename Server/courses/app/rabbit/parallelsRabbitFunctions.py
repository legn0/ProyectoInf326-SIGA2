import time
import pika as pk
import json
from pika.adapters.blocking_connection import BlockingChannel
import pika.exceptions as pkex
from .rabbitPublisher import create_rabbit_connection

def publishNewParallel(course_id: int, course_name: str, parallel_id: int, parallel_number: int, limite_cupo: int, jornada: int, campus_sede: int,
                        channel: BlockingChannel):
    '''
    Publica un mensaje cuando se crea un paralelo.
    Args:
        
        course_id (int): El ID único del curso.
        course_name (str): El nombre del curso.
        parallel_id(int): El ID del paralelo.
        parallel_number(int): número del paralelo.
        limite_cupo(int): limite de estudiantes en el paralelo.
        jornada(int): indica si es jornada diurno (1) o vespertino (2).
        campus_sede(int): Indca si es sede Casa Central (1), San Joaquin (2), Vitacura (3), Viña del mar (4) o Concepción (5)
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.
        
        

    Returns:
        None

    '''
    body =  {
        "curso" : {
            "id" : course_id,
            "name": course_name
        },
        "numero": parallel_number,
        "limite_cupo": limite_cupo,
        "jornada": jornada,
        "campus_sede": campus_sede
    }

    try:
        channel.basic_publish(exchange="courses",
                            routing_key=f"parallel.{parallel_id}.created",
                            body=json.dumps(body)
                            )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()
        publishNewParallel(course_id, course_name, parallel_id, parallel_number, limite_cupo, jornada, campus_sede, chan)

def publishUpdatedParallel( channel: BlockingChannel,
                            course_id: int, course_name: str,
                            parallel_id: int, number: int = None,
                            limite_cupo: int = None, jornada: int = None, Campus: int = None):
    '''
    Publica un mensaje cuando se actualiza un paralelo.
    Args:
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.
        course_id (int): El ID único del curso.
        course_name (str): El nombre del curso.
        parallel_id(int): El ID del paralelo.
        number(int): número del paralelo.
        limite_cupo(int): limite de estudiantes en el paralelo.
        jornada(int): indica si es jornada diurno (1) o vespertino (2).
        campus(int): Indca si es sede Casa Central (1), San Joaquin (2), Vitacura (3), Viña del mar (4) o Concepción (5)
        
        
    Returns:
        None

    '''

    body ={
        "curso" : {
            "id" : course_id,
            "name": course_name}
        }
    if number != None: body["numero"] = number
    if limite_cupo != None: body["limite_cupo"] = limite_cupo
    if jornada != None: body["jornada"] = jornada
    if Campus != None: body["campus_sede"] = Campus

    try:
        channel.basic_publish(
            exchange="courses",
            routing_key=f"parallel.{parallel_id}.updated",
            body=json.dumps(body)
        )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()

        publishUpdatedParallel(chan, course_id, course_name, parallel_id, number, limite_cupo, jornada, Campus)

def publishDeletedParallel(channel: BlockingChannel,
                           parallel_id: int, course_id: int, course_name: str):
    '''
    Publica un mensaje cuando se elimina un paralelo.
    Args:
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.
        parallel_id(int): El ID del paralelo.
        course_id (int): El ID único del curso.
        course_name (str): El nombre del curso.
        
    Returns:
        None

    ''' 
    
    body = {
        "curso" : {
            "id" : course_id,
            "name": course_name}
        }
    try:
        channel.basic_publish(
            exchange="courses",
            routing_key=f"parallel.{parallel_id}.deleted",
            body=json.dumps(body)
        )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()
        publishDeletedParallel(chan, parallel_id, course_id, course_name)
