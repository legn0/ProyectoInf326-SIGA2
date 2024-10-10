
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
import Classes
import uvicorn
import pyodbc

app = FastAPI()

db_config = {
    'user': '',
    'password': '',
    'host': '',  # or your MySQL server address
    'database': ''
}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules") ##Crear horario para un paralelo
def create_schedule(course_id: int, parallel_id: int, horario: Classes.Horario):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM bloques_horario WHERE nombre = %s", horario.nombre_bloque)
        id_bloque = cursor.fetchone()
        if id_bloque == None:
            return "Bloque no encontrado"
        id_bloque = id_bloque[0]
        cursor.execute("INSERT INTO horarios (course_id, parallel_id, bloque_id, tipo_bloque, is_deleted) VALUES (%s, %s, %s, %s, %s)", course_id, parallel_id, id_bloque, horario.tipo_bloque, 0)
        conn.commit()
        return "Horario creado con exito"
    finally:
        cursor.close()
        conn.close

@app.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Actualizar informacion de un horario
def update_schedule(course_id: int, parallel_id: int, schedule_id: int, horario: Classes.Horario):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if horario.tipo_bloque is not None and horario.id_bloque is not None:
        try:
            cursor.execute("UPDATE horarios SET bloque_id = %s, tipo_bloque = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", horario.id_bloque, horario.tipo_bloque, schedule_id)
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            return "Horario y tipo de bloque actualizado con exito"
    
    elif horario.tipo_bloque is not None and horario.id_bloque is None:
        try:
            cursor.execute("UPDATE horarios SET tipo_bloque = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", horario.tipo_bloque, schedule_id)
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            return "Tipo de bloque actualizado con exito"
    
    elif horario.tipo_bloque is None and horario.id_bloque is not None:
        try:
            cursor.execute("UPDATE horarios SET bloque_id = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", horario.id_bloque, schedule_id)
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            return "Horario actualizado con exito"
    
        

@app.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Eliminar horario
def delete_schedule(course_id: int, parallel_id: int, schedule_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM horarios WHERE id = %s", schedule_id)
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        return "Horario eliminado con exito"

@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules/{schedule_id}") ##Obtener informacion de un horario
def get_info_schedule(course_id: int, parallel_id: int, schedule_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM horarios WHERE id = %s", schedule_id)
        row = cursor.fetchone()
        if row == None:
            return "Horario no encontrado"
        else:
            columns = [column[0] for column in cursor.description]
            row = dict(zip(columns, row))
            return row
    finally:
        cursor.close()
        conn.close()

@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/schedules") ##Listar todos los horarios de un paralelo
def get_parallel_schedule(course_id: int, parallel_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM horarios WHERE parallel_id = %s", parallel_id)
        rows = cursor.fetchall()
        if rows == None:
            return "No hay horarios disponibles"
        else:
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in rows]
            return rows
    finally:
        cursor.close()
        conn.close()