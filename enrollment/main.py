from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
import pika

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def notify_event(event: str, body: str):
    """Función para enviar un mensaje a RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declarar una cola (asegurarse de que existe)
    channel.queue_declare(queue='enrollment_notifications')

    # Publicar un mensaje con la clave de enrutamiento basada en el evento
    channel.basic_publish(exchange='', routing_key=event, body=body)
    print(f" [x] Sent {event}: {body}")

    connection.close()

# Consultar una inscripción
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=schemas.Enrollment)
def read_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.id == enrollment_id,
            models.Enrollment.course_id == course_id,
            models.Enrollment.parallel_id == parallel_id,
            models.Enrollment.is_active == True
        )
        .first()
    )
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return db_enrollment

# Listar todas las inscripciones de un paralelo
@app.get("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=list[schemas.Enrollment])
def list_enrollments(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.course_id == course_id,
            models.Enrollment.parallel_id == parallel_id,
            models.Enrollment.is_active == True
        )
        .all()
    )

# Crear una nueva inscripción
@app.post("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments", response_model=schemas.Enrollment)
def create_enrollment(course_id: int, parallel_id: int, enrollment_request: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Verificar si el estudiante ya está inscrito en este curso
    existing_enrollment_course = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.student_id == enrollment_request.student_id,
            models.Enrollment.course_id == course_id,
            models.Enrollment.is_active == True
        )
        .first()
    )
    if existing_enrollment_course:
        raise HTTPException(status_code=400, detail="Estudiante ya inscrito en este curso")

    # Crear la inscripción
    enrollment_data = models.Enrollment(
        course_id=course_id,
        parallel_id=parallel_id,
        student_id=enrollment_request.student_id,
        is_active=True
    )
    db.add(enrollment_data)
    db.commit()
    db.refresh(enrollment_data)

    notify_event(f"enrollment.{enrollment_data.id}.created", f"Enrollment {enrollment_data.id} has been created.")
    return enrollment_data

# Actualizar una inscripción existente
@app.put("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}", response_model=schemas.Enrollment)
def update_enrollment(course_id: int, parallel_id: int, enrollment_id: int, enrollment_request: schemas.EnrollmentUpdate, db: Session = Depends(get_db)):
    db_enrollment = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.id == enrollment_id,
            models.Enrollment.course_id == course_id,
            models.Enrollment.parallel_id == parallel_id,
        )
        .first()
    )
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    db_enrollment.course_id = enrollment_request.course_id
    db_enrollment.parallel_id = enrollment_request.parallel_id
    db_enrollment.is_active = enrollment_request.is_active
    db.commit()
    db.refresh(db_enrollment)

    notify_event(f"enrollment.{db_enrollment.id}.updated", f"Enrollment {db_enrollment.id} has been updated.")
    return db_enrollment

# Eliminar una inscripción
@app.delete("/api/v1/courses/{course_id}/parallels/{parallel_id}/enrollments/{enrollment_id}")
def delete_enrollment(course_id: int, parallel_id: int, enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.id == enrollment_id,
            models.Enrollment.course_id == course_id,
            models.Enrollment.parallel_id == parallel_id,
            models.Enrollment.is_active == True
        )
        .first()
    )
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    db_enrollment.is_active = False
    db.commit()
    db.refresh(db_enrollment)
    notify_event(f"enrollment.{db_enrollment.id}.deleted", f"Enrollment {db_enrollment.id} has been deleted.")
    return {"message": "Inscripción eliminada exitosamente", "enrollment": db_enrollment}