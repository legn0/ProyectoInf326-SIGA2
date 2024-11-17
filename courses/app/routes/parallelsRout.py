from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database.db import get_db
from ..models import parallelsModel, coursesModel
from ..schemas import parallelsSchemas

# from ..rabbit.rabbitPublisher import get_rabbit_channel
# from pika.adapters.blocking_connection import BlockingChannel
# from ..rabbit.parallelsRabbitFunctions import *

router = APIRouter(
    prefix="/api/v1/courses/{course_id}/parallels",
    tags=["Parallels"]
)

# Crear un paralelo
@router.post("/", response_model=parallelsSchemas.Parallel, status_code=status.HTTP_201_CREATED)
def create_parallel(course_id: int, parallel: parallelsSchemas.ParallelCreate, db: Session = Depends(get_db),
                    #channel: BlockingChannel = Depends(get_rabbit_channel)
                    ):
    """
    Crea un nuevo paralelo para un curso específico.

    Args:
        course_id (int): El ID del curso al que pertenece el paralelo.
        parallel (ParallelCreate): Los datos del paralelo que se va a crear.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        Parallel: El paralelo recién creado.

    Raises:
        HTTPException: Si el curso no se encuentra.

    Este endpoint permite crear un nuevo paralelo y luego publica un mensaje en RabbitMQ indicando que el paralelo fue creado.
    """
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_course or db_course.is_deleted:
        raise HTTPException(status_code=404, detail="Course not found")

    db_parallel = parallelsModel.Parallel(**parallel.dict(), course_id=course_id)
    db.add(db_parallel)
    db.commit()
    db.refresh(db_parallel)
    # publishNewParallel(course_id=course_id,
    #                     course_name=db_course.name,
    #                     parallel_id=db_parallel.id,
    #                     parallel_number=db_parallel.number,
    #                     limite_cupo=db_parallel.limite_cupo,
    #                     jornada=db_parallel.jornada,
    #                     campus_sede=db_parallel.Campus,
    #                     channel=channel)
    return db_parallel

# Actualizar un paralelo
@router.put("/{parallel_id}", response_model=parallelsSchemas.Parallel)
def update_parallel(course_id: int, parallel_id: int, parallel: parallelsSchemas.ParallelUpdate, db: Session = Depends(get_db),
                    #channel: BlockingChannel = Depends(get_rabbit_channel)
                    ):
    """
    Actualiza un paralelo existente para un curso específico.

    Args:
        course_id (int): El ID del curso al que pertenece el paralelo.
        parallel_id (int): El ID del paralelo que se va a actualizar.
        parallel (ParallelUpdate): Los nuevos datos del paralelo.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        Parallel: El paralelo actualizado.

    Raises:
        HTTPException: Si no se encuentra el curso o el paralelo.

    Este endpoint actualiza un paralelo existente y luego publica un mensaje en RabbitMQ indicando que el paralelo fue actualizado.
    """
    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    if not db_parallel:
        raise HTTPException(status_code=404, detail="Parallel not found")

    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_course or db_course.is_deleted:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in parallel.dict(exclude_unset=True).items():
        setattr(db_parallel, key, value)

    db.commit()
    db.refresh(db_parallel)

    # publishUpdatedParallel(channel = channel,
    #                        course_id=course_id,
    #                        course_name=db_course.name,
    #                        parallel_id=parallel_id,
    #                        **parallel.dict(exclude_unset=True) 
    #                        )
    return db_parallel

# Eliminar un paralelo
@router.delete("/{parallel_id}")
def delete_parallel(course_id: int, parallel_id: int, db: Session = Depends(get_db),
                    #channel: BlockingChannel = Depends(get_rabbit_channel)
                    ):
    """
    Elimina un paralelo existente de un curso.

    Args:
        course_id (int): El ID del curso al que pertenece el paralelo.
        parallel_id (int): El ID del paralelo que se va a eliminar.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        dict: Un mensaje indicando que el paralelo fue eliminado.

    Raises:
        HTTPException: Si no se encuentra el curso o el paralelo.

    Este endpoint elimina un paralelo y publica un mensaje en RabbitMQ indicando que el paralelo fue eliminado.
    """
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    if not db_parallel:
        raise HTTPException(status_code=404, detail="Parallel not found")
    # publishDeletedParallel(channel = channel,
    #                        parallel_id=parallel_id,
    #                        course_id=course_id,
    #                        course_name=db_course.name)
    db_parallel.is_deleted = True
    db.commit()
    db.refresh(db_parallel)
    return {"message": "Parallel deleted successfully"}

# Consultar un paralelo
@router.get("/{parallel_id}", response_model=parallelsSchemas.Parallel)
def get_parallel(course_id: int, parallel_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un paralelo específico de un curso.

    Args:
        course_id (int): El ID del curso al que pertenece el paralelo.
        parallel_id (int): El ID del paralelo que se desea consultar.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        Parallel: El paralelo encontrado.

    Raises:
        HTTPException: Si no se encuentra el curso o el paralelo.

    Este endpoint obtiene los detalles de un paralelo específico de un curso.
    """
    db_parallel = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.id == parallel_id, parallelsModel.Parallel.course_id == course_id).first()
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_parallel or db_parallel.is_deleted:
        raise HTTPException(status_code=404, detail="Parallel not found")
    if not db_course or db_course.is_deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_parallel

# Listar todos los paralelos de un curso
@router.get("/", response_model=List[parallelsSchemas.Parallel])
def get_parallels(course_id: int, db: Session = Depends(get_db)):
    """
    Lista todos los paralelos de un curso.

    Args:
        course_id (int): El ID del curso cuyos paralelos se desean listar.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        List[Parallel]: Una lista de todos los paralelos asociados a un curso.

    Este endpoint devuelve una lista de todos los paralelos asociados a un curso específico.
    """
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == course_id).first()
    if not db_course or db_course.is_deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    db_parallels = db.query(parallelsModel.Parallel).filter(parallelsModel.Parallel.course_id == course_id, parallelsModel.Parallel.is_deleted == False).all()
    return db_parallels
