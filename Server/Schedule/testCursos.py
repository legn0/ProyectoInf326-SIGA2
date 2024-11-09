import pika
import json

##Routing key puede ser 'course/parallel.id.created/updated/deleted'

def publish_test_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='courses', exchange_type='topic')

    
    message =  {
        "curso" : {
            "id" : 7,
            "name": "Prueba"
        },
        "numero": 200, #Numero del paralelo distinto al id
        "limite_cupo": 40,
        "jornada": 1, #1 diurno 2 vespertino
        "campus_sede": 2 # 1=cc, 2=sj, 3=vita, 4=vina, 5=conce
    }
    channel.basic_publish(
        exchange='courses',
        routing_key='parallel.84.created',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent 'Test Message'")
    connection.close()

if __name__ == "__main__":
    publish_test_message()

    