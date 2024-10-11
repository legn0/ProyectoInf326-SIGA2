import pika as pk


conn = pk.BlockingConnection(pk.URLParameters(f"amqp://guest:guest@localhost:5672/%2f?heartbeat=2400")) #Coneccion con rabbit
chan = conn.channel()


chan.exchange_declare(  exchange="courses", #Creacion de topico
                        exchange_type="topic"
                        ) 

queue = chan.queue_declare('testing_queue')
queue_name = queue.method.queue

chan.queue_bind(
    exchange="courses",
    queue=queue_name,
    routing_key='parallel.*.updated'
)

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}: {body}")

chan.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

chan.start_consuming()