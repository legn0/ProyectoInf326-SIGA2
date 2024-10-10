import pika as pk
import json
from pika.adapters.blocking_connection import BlockingChannel

def publishNewParallel(course_id: int, course_name: str, parallel_id: int, parallel_number: int, limite_cupo: int, jornada: int, campus_sede: int,
                        channel: BlockingChannel):
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

    channel.basic_publish(exchange="courses",
                          routing_key=f"parallel.{parallel_id}.created",
                          body=json.dumps(body)
                          )


def publishUpdatedParallel( channel: BlockingChannel,
                            course_id: int, course_name: str,
                            parallel_id: int, number: int = None,
                            limite_cupo: int = None, jornada: int = None, Campus: int = None):

    body ={
        "curso" : {
            "id" : course_id,
            "name": course_name}
        }
    if number != None: body["numero"] = number
    if limite_cupo != None: body["limite_cupo"] = limite_cupo
    if jornada != None: body["jornada"] = jornada
    if Campus != None: body["campus_sede"] = Campus

    channel.basic_publish(
        exchange="courses",
        routing_key=f"parallel.{parallel_id}.updated",
        body=json.dumps(body)
    )

def publishDeletedParallel(channel: BlockingChannel,
                           parallel_id: int, course_id: int, course_name: str):
    
    body = {
        "curso" : {
            "id" : course_id,
            "name": course_name}
        }

    channel.basic_publish(
        exchange="courses",
        routing_key=f"parallel.{parallel_id}.deleted",
        body=json.dumps(body)
    )