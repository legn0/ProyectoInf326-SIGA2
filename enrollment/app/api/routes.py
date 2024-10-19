import pika
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.schemas import Enrollment, EnrollmentCreate, EnrollmentUpdate
from ..crud.crud import EnrollmentCRUD
from .external_calls import ExternalCourseAPI
import os

router = APIRouter()

def notify_event(event: str, body: str):
    """Función para enviar un mensaje a RabbitMQ."""
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
    channel = connection.channel()
    # Declarar una cola (asegurarse de que existe)
    channel.queue_declare(queue='enrollment_notifications')
    # Publicar un mensaje con la clave de enrutamiento basada en el evento
    channel.basic_publish(exchange='', routing_key=event, body=body)
    print(f" [x] Sent {event}: {body}")
    connection.close()

# Consultar una inscripción
@router.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=Enrollment)
def read_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
    enrollment = crud.get_enrollment(enrollment_id, course_id, parallel_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return enrollment

# Listar todas las inscripciones de un paralelo
@router.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=list[Enrollment])
def list_enrollments(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
    return crud.list_enrollments(course_id, parallel_id)

# Crear una nueva inscripción
@router.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=Enrollment)
def create_enrollment(course_id: int, parallel_id: int, enrollment_request: EnrollmentCreate, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
     # Verificar si el estudiante ya está inscrito en el curso y paralelo
    existing_enrollment = crud.get_enrollment_by_student_and_course(enrollment_request.student_id, course_id, parallel_id)
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="El estudiante ya está inscrito en este curso y paralelo")
    # Crear la inscripción
    enrollment_data = crud.create_enrollment(course_id, parallel_id, enrollment_request)
    # Enviar notificación a RabbitMQ
    notify_event(f"enrollment.{enrollment_data.id}.created", f"Enrollment {enrollment_data.id} has been created.")
    return enrollment_data

# Actualizar una inscripción existente
@router.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=Enrollment)
def update_enrollment(course_id: int, parallel_id: int, enrollment_id: int, enrollment_request: EnrollmentUpdate, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
    enrollment_data = crud.update_enrollment(enrollment_id, enrollment_request)
    if enrollment_data is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    notify_event(f"enrollment.{enrollment_data.id}.updated", f"Enrollment {enrollment_data.id} has been updated.")
    return enrollment_data

# Eliminar una inscripción
@router.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}")
def delete_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
    deleted = crud.delete_enrollment(enrollment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    notify_event(f"enrollment.{enrollment_id.id}.deleted", f"Enrollment {enrollment_id.id} has been deleted.")
    return {"message": "Inscripción eliminada exitosamente", "enrollment": deleted}

#Realizar una ronda de inscripción
@router.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/round", response_model=list[Enrollment])
def enroll_students_round(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    crud = EnrollmentCRUD(db)
    external_api = ExternalCourseAPI()

    # Obtener el límite de cupos desde la API externa
    try:
        parallel_data = external_api.get_parallel_data(course_id, parallel_id)  
        cupos = parallel_data["limite_cupos"]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Consultar los estudiantes con estado "Pendiente"
    pending_enrollments = crud.get_pending_enrollments(course_id, parallel_id)
    
    if not pending_enrollments:
        raise HTTPException(status_code=404, detail="No hay inscripciones pendientes para este curso y paralelo")

    # Inscribir hasta el límite de cupos disponibles
    number_to_enroll = min(cupos, len(pending_enrollments))
    selected_enrollments = random.sample(pending_enrollments, number_to_enroll)

    # Actualizar el estado de las inscripciones seleccionadas a 'Inscrita'
    updated_enrollments = []
    for enrollment in selected_enrollments:
        enrollment.is_active = "Inscrita"  # Cambiar el estado a "Inscrita"
        updated_enrollment = crud.update_enrollment_status(enrollment.id, enrollment)
        updated_enrollments.append(updated_enrollment)

    return updated_enrollments