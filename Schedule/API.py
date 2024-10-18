from fastapi import FastAPI, HTTPException
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import Classes
import uvicorn
import pika
import json
import os
import logging


app = FastAPI()

db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'admin'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'horarios')
}

rabbitmq_config = {
    'host': os.getenv('RABBITMQ_HOST', 'localhost'),
    'exchange': os.getenv('RABBITMQ_EXCHANGE', 'horario_events'),
    'exchange_type': os.getenv('RABBITMQ_EXCHANGE_TYPE', 'topic')
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


##Conexión a RabbitMQ

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_config['host']))
    channel = connection.channel()
    channel.exchange_declare(exchange=rabbitmq_config['exchange'], exchange_type=rabbitmq_config['exchange_type'])
    channel.queue_declare(queue='horario_events', durable=True)
    channel.queue_bind(exchange=rabbitmq_config['exchange'], queue='horario_events', routing_key='schedule.*.*')
except pika.exceptions.AMQPConnectionError as e:
    logger.error(f"Failed to connect to RabbitMQ: {e}")
    raise

##Función para emitir eventos con RabbitMQ

def emit_event(routing_key: str, body: dict):
    try:
        channel.basic_publish(
            exchange=rabbitmq_config['exchange'],
            routing_key=routing_key,
            body=json.dumps(body)
        )
        logger.info(f"Evento emitido: {routing_key}")
    except Exception as e:
        logger.error(f"Error al emitir evento: {e}")

if __name__ == "__main__":
    try: 
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        connection.close()

#Crear un nuevo horario para un paralelo específico

@app.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules", status_code=201)
def create_schedule(course_id: int, parallel_id: int, horario: Classes.Horario):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si ya existe un horario para el course_id y parallel_id que no esté eliminado
        cursor.execute("""
            SELECT id, bloque_id, tipo FROM horarios
            WHERE course_id = %s AND parallel_id = %s AND is_deleted = 0
        """, (course_id, parallel_id))
        existing_schedule = cursor.fetchone()
        
        if not existing_schedule:
            # Si no existe un horario, devolver un error
            raise HTTPException(status_code=404, detail="No se encontró un horario para este paralelo y curso.")
        
        bloque_id = None
        if horario.nombre_bloque:
            cursor.execute("SELECT id FROM bloques_horario WHERE nombre = %s", (horario.nombre_bloque,))
            bloque = cursor.fetchone()
            if not bloque:
                raise HTTPException(status_code=404, detail=f"Bloque '{horario.nombre_bloque}' no encontrado")
            bloque_id = bloque['id']
        elif horario.id_bloque:
            cursor.execute("SELECT id FROM bloques_horario WHERE id = %s", (horario.id_bloque,))
            bloque = cursor.fetchone()
            if not bloque:
                raise HTTPException(status_code=404, detail=f"Bloque con ID '{horario.id_bloque}' no encontrado")
            bloque_id = horario.id_bloque
        
        update_fields = []
        update_values = []
        if bloque_id is not None:
            update_fields.append("bloque_id = %s")
            update_values.append(bloque_id)
        if horario.tipo is not None:
            update_fields.append("tipo = %s")
            update_values.append(horario.tipo)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
        
        update_values.append(existing_schedule['id'])
        update_query = f"""
            UPDATE horarios
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(update_query, tuple(update_values))
        conn.commit()
        
        # Emitir evento de actualización
        event_routing_key = f"schedule.{existing_schedule['id']}.updated"
        event_body = {
            "schedule_id": existing_schedule['id'],
            "course_id": course_id,
            "parallel_id": parallel_id,
            "bloque_id": bloque_id if bloque_id is not None else existing_schedule['bloque_id'],
            "tipo": horario.tipo if horario.tipo is not None else existing_schedule['tipo'],
            "is_deleted": False,
            "updated_at": datetime.now().isoformat()
        }
        emit_event(event_routing_key, event_body)
        
        return {"message": "Horario actualizado con éxito", "schedule_id": existing_schedule['id']}
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error al actualizar el horario")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#Actualizar la información de un horario existente
@app.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}")
def update_schedule(course_id: int, parallel_id: int, schedule_id: int, horario: Classes.Horario):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar que el horario existe y no está eliminado
        cursor.execute("""
            SELECT bloque_id, tipo FROM horarios
            WHERE id = %s AND course_id = %s AND parallel_id = %s AND is_deleted = 0
        """, (schedule_id, course_id, parallel_id))
        resultado = cursor.fetchone()
        if not resultado:
            raise HTTPException(status_code=404, detail="Horario no encontrado")

        bloque_id_actual, tipo_actual = resultado

        # Determinar si se actualizará el bloque
        if horario.nombre_bloque:
            cursor.execute("SELECT id FROM bloques_horario WHERE nombre = %s", (horario.nombre_bloque,))
            bloque = cursor.fetchone()
            if not bloque:
                raise HTTPException(status_code=404, detail="Bloque no encontrado")
            bloque_id = bloque[0]

        elif horario.id_bloque:
            cursor.execute("SELECT id FROM bloques_horario WHERE id = %s", (horario.id_bloque,))
            bloque = cursor.fetchone()
            if not bloque:
                raise HTTPException(status_code=404, detail="Bloque no encontrado")
            bloque_id = horario.id_bloque

        else:
            bloque_id = bloque_id_actual

        # Determinar si se actualizará el tipo
        tipo = horario.tipo if horario.tipo is not None else tipo_actual

        # Actualizar el horario en la base de datos
        update_query = """
            UPDATE horarios
            SET bloque_id = %s, tipo = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(update_query, (bloque_id, tipo, schedule_id))
        conn.commit()

        # Emisión del evento de actualización
        event_routing_key = f"schedule.{schedule_id}.updated"
        event_body = {
            "schedule_id": schedule_id,
            "course_id": course_id,
            "parallel_id": parallel_id,
            "bloque_id": bloque_id,
            "tipo": tipo,
            "is_deleted": False,
            "updated_at": datetime.now().isoformat()
        }
        emit_event(event_routing_key, event_body)

        return {"message": "Horario actualizado con exito"}
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error al actualizar el horario")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#Eliminar (soft delete) un horario existente
@app.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}")
def delete_schedule(course_id: int, parallel_id: int, schedule_id: int):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar que el horario existe y no está eliminado
        cursor.execute("""
            SELECT is_deleted FROM horarios
            WHERE id = %s AND course_id = %s AND parallel_id = %s
        """, (schedule_id, course_id, parallel_id))
        resultado = cursor.fetchone()
        if not resultado:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        is_deleted = resultado[0]
        if is_deleted:
            raise HTTPException(status_code=400, detail="Horario ya está eliminado")

        # Eliminar el horario (soft delete) en la base de datos
        cursor.execute("""
            UPDATE horarios
            SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (schedule_id,))
        conn.commit()

        # Emisión del evento de eliminación
        event_routing_key = f"schedule.{schedule_id}.deleted"
        event_body = {
            "schedule_id": schedule_id,
            "course_id": course_id,
            "parallel_id": parallel_id,
            "is_deleted": True,
            "deleted_at": datetime.now().isoformat()
        }
        emit_event(event_routing_key, event_body)

        return {"message": "Horario eliminado con exito (soft delete)"}
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error al eliminar el horario")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#Obtener información detallada de un horario específico
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}")
def get_info_schedule(course_id: int, parallel_id: int, schedule_id: int):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consultar información del horario junto con el nombre del bloque y las horas en formato string
        cursor.execute("""
            SELECT h.id, h.course_id, h.parallel_id, h.bloque_id, b.nombre AS bloque_nombre,
                   h.tipo, h.is_deleted, h.created_at, h.updated_at,
                   b.hora_inicio,  -- Aquí se obtiene directamente como string
                   b.hora_fin     -- Aquí también como string
            FROM horarios h
            LEFT JOIN bloques_horario b ON h.bloque_id = b.id
            WHERE h.id = %s AND h.course_id = %s AND h.parallel_id = %s AND h.is_deleted = 0
        """, (schedule_id, course_id, parallel_id))

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        else:
            columnas = [column[0] for column in cursor.description]
            horario_info = dict(zip(columnas, row))

            # Devolver la información del horario junto con la hora de inicio y fin del bloque como strings
            return horario_info

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error al obtener el horario")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

            
#Listar todos los horarios de un paralelo específico
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules")
def get_parallel_schedule(course_id: int, parallel_id: int):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consultar todos los horarios del paralelo que no están eliminados
        cursor.execute("""
            SELECT h.id, h.course_id, h.parallel_id, h.bloque_id, b.nombre AS bloque_nombre,
                   h.tipo, h.is_deleted, h.created_at, h.updated_at
            FROM horarios h
            LEFT JOIN bloques_horario b ON h.bloque_id = b.id
            WHERE h.course_id = %s AND h.parallel_id = %s AND h.is_deleted = 0
            ORDER BY h.created_at DESC
        """, (course_id, parallel_id))
        rows = cursor.fetchall()
        if not rows:
            return {"message": "No hay horarios disponibles"}
        else:
            columnas = [column[0] for column in cursor.description]
            horarios = [dict(zip(columnas, row)) for row in rows]
            return horarios
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error al listar los horarios")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

