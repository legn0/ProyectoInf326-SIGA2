from fastapi.testclient import TestClient
from API import app
from Classes import Horario

client = TestClient(app)

# Test POST
def test_create_or_update_schedule_success():
    horario = {
        "id_bloque": 1,
        "nombre_bloque": "1-2",
        "tipo": "Clase",
        "id_profesor": 1,
        "nombre_profesor": "Profesor X",
        "dia": "Lunes"
    }
    response = client.post("/api/v1/courses/15/parallels/15/schedules", json=horario)
    assert response.status_code == 201
    assert response.json()["message"] == "Horario creado con éxito" or "Horario actualizado con éxito"

def test_create_or_update_schedule_not_found():
    horario = {
        "id_bloque": 9999,  # Bloque id no deberia exisitr
        "nombre_bloque": "Non-existent", # Bloque name no deberia exisitr
        "tipo": "Prueba",
        "id_profesor": 1,
        "nombre_profesor": "Profesor X",
        "dia": "Lunes"
    }
    response = client.post("/api/v1/courses/15/parallels/15/schedules", json=horario)
    assert response.status_code == 404

def test_create_or_update_schedule_bad_request(): #Falta id_bloque
    horario = {
        "nombre_bloque": "1-2",
        "tipo": "Clase",
        "id_profesor": 1,
        "nombre_profesor": "Profesor X",
        "dia": "Lunes"
    }
    response = client.post("/api/v1/courses/15/parallels/15/schedules", json=horario)
    assert response.status_code == 422

# Test PUT
def test_update_schedule_success():
    horario = {
        "id_bloque": 1,
        "nombre_bloque": "1-2",
        "tipo": "Clase",
        "id_profesor": 1,
        "nombre_profesor": "Profesor Actualizado",
        "dia": "Lunes"
    }
    response = client.put("/api/v1/courses/1/parallels/200/schedules/1", json=horario)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado con éxito"

def test_update_schedule_not_found():
    horario = {
        "id_bloque": 1,
        "nombre_bloque": "1-2",
        "tipo": "Clase",
        "id_profesor": 1,
        "nombre_profesor": "Profesor Actualizado",
        "dia": "Lunes"
    }
    response = client.put("/api/v1/courses/1/parallels/200/schedules/9999", json=horario)  # Assumiendo scheduke_id no existe
    assert response.status_code == 404

def test_update_schedule_bad_request():
    horario = {
        "nombre_bloque": "1-2",
        "tipo": "Clase",
        "id_profesor": 1,
        "nombre_profesor": "Profesor Actualizado",
        "dia": "Lunes"
    }
    response = client.put("/api/v1/courses/1/parallels/200/schedules/1", json=horario)
    assert response.status_code == 422


# Test GET 1
def test_get_info_schedule_success():
    response = client.get("/api/v1/courses/1/parallels/200/schedules/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_info_schedule_not_found():
    response = client.get("/api/v1/courses/1/parallels/200/schedules/9999")  # schedule_id no existe
    assert response.status_code == 404

def test_get_info_schedule_bad_request():
    response = client.get("/api/v1/courses/1/parallels/200/schedules/abc")  # schedule_id invalido
    assert response.status_code == 422

# Test GET 2
def test_get_parallel_schedule_success():
    response = client.get("/api/v1/courses/1/parallels/200/schedules")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_parallel_schedule_not_found():
    response = client.get("/api/v1/courses/9999/parallels/9999/schedules")  # course_id and parallel_id no existen
    assert response.status_code == 200
    assert response.json() == {"message": "No hay horarios disponibles"}

def test_get_parallel_schedule_bad_request():
    response = client.get("/api/v1/courses/abc/parallels/abc/schedules")  # course_id and parallel_id invalidos
    assert response.status_code == 422

# Test DELETE
def test_delete_schedule_success():
    response = client.delete("/api/v1/courses/1/parallels/200/schedules/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado con exito (soft delete)"

def test_delete_schedule_not_found():
    response = client.delete("/api/v1/courses/1/parallels/1/schedules/9999")  # schedule_id no existe
    assert response.status_code == 404

def test_delete_schedule_bad_request():
    response = client.delete("/api/v1/courses/1/parallels/1/schedules/abc") # schedule_id invalido
    assert response.status_code == 422