import time
import pika as pk
import json
from pika.adapters.blocking_connection import BlockingChannel
import pika.exceptions as pkex
from .rabbitPublisher import create_rabbit_connection

def publishCreateCourse(course_name: str, sigla: str, creditos: int, departamento:str, prerequisitos: str, course_id: int,
                        channel: BlockingChannel):
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
    except pkex.StreamLostError:
        time.sleep(2)
        create_rabbit_connection()
        channel.basic_publish(exchange="courses",
                            routing_key=f"course.{course_id}.created",
                            body=json.dumps(body)
        )

def publishUpdatedCourse(channel: BlockingChannel, 
                         course_id: int,
                         name: str = None,
                         sigla: str = None,
                         creditos: int = None,
                         departamento: str = None,
                         prerequisites: str = None):

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
    except pkex.StreamLostError:
        time.sleep(2)
        create_rabbit_connection()
        channel.basic_publish(
            exchange="courses",
            routing_key=f"course.{course_id}.updated",
            body=json.dumps(body)
        )
    

def publishDeletedCourse(channel: BlockingChannel,
                           course_id: int):
    body = {}

    try:
        channel.basic_publish(
            exchange="courses",
            routing_key=f"course.{course_id}.deleted",
            body=json.dumps(body)
        )
    except pkex.StreamLostError:
        time.sleep(2)
        create_rabbit_connection()
        channel.basic_publish(
            exchange="courses",
            routing_key=f"course.{course_id}.deleted",
            body=json.dumps(body)
        )   
  