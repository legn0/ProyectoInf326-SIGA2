import time
import pika as pk
import json
from pika.adapters.blocking_connection import BlockingChannel
import pika.exceptions as pkex
from .rabbitPublisher import create_rabbit_connection

def publishCreateCourse(course_name: str, sigla: str, creditos: int, departamento:str, prerequisitos: str, course_id: int,
                        channel: BlockingChannel):
    '''
    Publica un mensaje cuando se crea un nuevo curso.
    Args:
        course_name (str): El nombre del curso.
        sigla (str): La sigla del curso
        creditos (int): El número de créditos del curso.
        departamento (str): El departamento al que pertenece el curso.
        prerequisitos (str): Los prerequisitos del curso.
        course_id (int): El ID único del curso.
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.

    Returns:
        None

    '''
    body = {
        "name"          : course_name,
        "sigla"         : sigla,
        "creditos"      : creditos,
        "departamento"  : departamento,
        "prerequisitos" : prerequisitos
            

    }

    try:
        channel.basic_publish(exchange="courses",
                            routing_key=f"course.{course_id}.created",
                            body=json.dumps(body)
                            )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()
        publishCreateCourse(course_name, sigla, creditos, departamento, prerequisitos, course_id, chan)

def publishUpdatedCourse(channel: BlockingChannel, 
                         course_id: int,
                         name: str = None,
                         sigla: str = None,
                         creditos: int = None,
                         departamento: str = None,
                         prerequisites: str = None):
    '''
    Publica un mensaje cuando se actualiza curso.

    Args:
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.
        course_id (int): El ID único del curso.
        name (str): El nombre del curso.
        sigla (str): La sigla del curso
        creditos (int): El número de créditos del curso.
        departamento (str): El departamento al que pertenece el curso.
        prerequisites (str): Los prerequisitos del curso.    

    Returns:
        None

    '''

    body = {

    }

    if name != None: body["name"] = name
    if sigla != None: body["sigla"] = sigla
    if creditos != None: body["creditos"] = creditos
    if departamento != None: body["departamento"] = departamento
    if prerequisites != None: body["prerequisites"] = prerequisites

    try:
        channel.basic_publish(
            exchange="courses",
            routing_key=f"course.{course_id}.updated",
            body=json.dumps(body)
        )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()
        publishUpdatedCourse(chan, course_id, name, sigla, creditos, departamento, prerequisites)
    

def publishDeletedCourse(channel: BlockingChannel,
                           course_id: int):
    '''
    Publica un mensaje cuando se elimina un curso.
    Args:
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje.
        course_id (int): El ID único del curso.

    Returns:
        None

    '''
    body = {}

    try:
        channel.basic_publish(
            exchange="courses",
            routing_key=f"course.{course_id}.deleted",
            body=json.dumps(body)
        )
    except:
        time.sleep(2)
        chan = create_rabbit_connection()
        publishDeletedCourse(chan, course_id)   
  
