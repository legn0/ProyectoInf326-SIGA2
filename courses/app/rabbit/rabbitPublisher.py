import pika as pk
from pika.adapters.blocking_connection import BlockingChannel

rabbit_conn = None
rabbit_channel = None


def get_rabbit_channel() -> BlockingChannel:
    if rabbit_channel is None:
        raise RuntimeError("Canal no existe")
    return rabbit_channel

def create_rabbit_connection():
    global rabbit_channel, rabbit_conn
    
    rabbit_conn = pk.BlockingConnection(pk.URLParameters(f"amqp://guest:guest@rabbitmq:5672")) #Coneccion con rabbit
    rabbit_channel = rabbit_conn.channel()
    rabbit_channel.exchange_declare(exchange="courses", #Creacion de topico
                     exchange_type="topic"
                     )
def close_rabbit_connection():
    global rabbit_conn, rabbit_channel

    if rabbit_channel is not None:
        rabbit_channel.close()
    if rabbit_conn is not None:
        rabbit_conn.close()
