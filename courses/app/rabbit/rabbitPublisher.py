# import time
# import pika as pk
# from pika.adapters.blocking_connection import BlockingChannel
# import pika.exceptions as pkex
# import os

# rabbit_conn = None
# rabbit_channel = None
# RABBIT_USER = os.getenv("RABBIT_USER")
# RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")
# RABBIT_NAME = os.getenv("RABBIT_NAME")

# def get_rabbit_channel() -> BlockingChannel:
#     '''
#     Obtiene el canal a ser utilizado para operaciones de RabbitMQ
    
#     Args:
#         None
#     Returns:
#         BlockingChannel: Canal de RabbitMQ con el que se enviaran mensajes 
#     '''
    
#     global rabbit_conn, rabbit_channel
#     if rabbit_conn != None:
#         if  rabbit_conn.is_closed:
#             create_rabbit_connection()
#         elif rabbit_channel.is_closed:
#             rabbit_channel= rabbit_conn.channel()
#             rabbit_channel.exchange_declare(exchange="courses", #Creacion de topico
#                         exchange_type="topic"
#                         ) 
#     else:
#         create_rabbit_connection()
#     return rabbit_channel

# def create_rabbit_connection():
#     '''
#     Crea la coneccion y canal hacia el Broker de RabbitMQ

#     Args:
#         None
#     Returns:
#         None
#     '''
#     global rabbit_channel, rabbit_conn
#     def create_rabbit_connection_aux(tries: int):
#         '''
#         Funcion recursiva que trata hasta 5 veces de crear una conneccion y canal con el broker de RabbitMQ

#         Args: 
#             tries (int): Intentos actuales.

#         Returns:
#             None
        
#         '''
        
#         global rabbit_channel, rabbit_conn
#         try: 
#             rabbit_conn = pk.BlockingConnection(pk.URLParameters(f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_NAME}:5672/%2f?heartbeat=240")) #Coneccion con rabbit
#             rabbit_channel = rabbit_conn.channel()
#             rabbit_channel.exchange_declare(exchange="courses", #Creacion de topico
#                             exchange_type="topic"
#                             )
#         except (pkex.AMQPConnectionError, pkex.ChannelError):
#             if tries > 5:
#                 return False 
#             time.sleep(4)
#             return create_rabbit_connection_aux(tries=tries+1)     
#         return True
#     ret = create_rabbit_connection_aux(0)
#     return (rabbit_channel if ret else None)

# def close_rabbit_connection():
#     '''
#     Cierra el canal y coneccion con el broker RabbitMQ

#     Args:
#         None
#     Returns:
#         None
#     '''
    
#     global rabbit_conn, rabbit_channel

#     if rabbit_channel is not None:
#         rabbit_channel.close()
#     if rabbit_conn is not None:
#         rabbit_conn.close()
