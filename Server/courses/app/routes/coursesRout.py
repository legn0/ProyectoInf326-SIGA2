from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 

from ..models import coursesModel
from ..schemas import coursesSchemas 

from ..rabbit.rabbitPublisher import get_rabbit_channel

from pika.adapters.blocking_connection import BlockingChannel

from ..rabbit.courseRabbitFunctions import *

router = APIRouter(
    prefix="/api/v1/courses",
    responses={404: {"description": "Not found"}},
    tags=["Courses"]
)

@router.get("/", response_model=list[coursesSchemas.Course])
def get_courses(db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    """
    Obtiene todos los cursos almacenados en la base de datos.

    Args:
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        List[Course]: Una lista con todos los cursos en la base de datos.
    
    Este endpoint obtiene una lista de todos los cursos disponibles.
    """
    courses = db.query(coursesModel.Course).filter(coursesModel.Course.is_deleted == False).all()
    return courses

@router.get("/{id}", response_model=coursesSchemas.Course) #course por id
def get_course(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un curso específico por su ID.

    Args:
        id (int): El ID del curso que se desea obtener.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        Course: El curso encontrado por su ID.

    Raises:
        HTTPException: Si no se encuentra el curso con el ID proporcionado.

    Este endpoint obtiene un curso específico según el ID proporcionado en la URL.
    Si el curso no existe, se devuelve un error 404.
    """

    course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id).first()
    if not course or course.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=coursesSchemas.Course) #Crear course
def create_course(course: coursesSchemas.CourseCreate, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    """
    Crea un nuevo curso y lo publica en un sistema de mensajería.

    Args:
        course (CourseCreate): El esquema de los datos que se usarán para crear el curso.
        db (Session): La sesión de base de datos de SQLAlchemy proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        Course: El curso recién creado.

    Proceso:
    1. Se crea un curso en la base de datos utilizando los datos proporcionados.
    2. Se publica un mensaje en RabbitMQ indicando que se ha creado un nuevo curso.
    """
    db_course = coursesModel.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    publishCreateCourse(course_id = db_course.id,
                        course_name=db_course.name,
                        sigla= db_course.sigla,
                        creditos=db_course.creditos,
                        departamento=db_course.departamento,
                        prerequisitos=db_course.prerequisites,
                        channel=channel)
    return db_course

@router.put("/{id}", response_model=coursesSchemas.Course) #Actualizar course
def update_course(id: int, course: coursesSchemas.CourseUpdate, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    """
    Actualiza un curso existente.

    Args:
        id (int): El ID del curso que se va a actualizar.
        course (CourseUpdate): El esquema de los datos para actualizar el curso.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        Course: El curso actualizado.

    Raises:
        HTTPException: Si no se encuentra el curso con el ID proporcionado.

    Proceso:
    1. Se busca el curso en la base de datos por su ID.
    2. Si no se encuentra, se lanza una excepción 404.
    3. Si el curso existe, se actualizan los datos proporcionados.
    4. Se publica un mensaje en RabbitMQ indicando que el curso fue actualizado.
    """
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id)
    if not db_course or db_course.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db_course.update(course.dict(), synchronize_session=False)
    db.commit()
    publishUpdatedCourse(channel=channel,
                         course_id=db_course.first().id,
                         **course.dict(exclude_unset=True))
    return db_course.first()

@router.delete("/{id}", response_model=coursesSchemas.Course) #Eliminar course
def delete_course(id: int, db: Session = Depends(get_db), channel: BlockingChannel = Depends(get_rabbit_channel)):
    """
    Elimina un curso existente.

    Args:
        id (int): El ID del curso que se va a eliminar.
        db (Session): La sesión de base de datos proporcionada por la dependencia `get_db`.
        channel (BlockingChannel): El canal de RabbitMQ para publicar el mensaje proporcionado por la dependencia `get_rabbit_channel`.

    Returns:
        Course: El curso eliminado.

    Raises:
        HTTPException: Si no se encuentra el curso con el ID proporcionado.

    Proceso:
    1. Se busca el curso en la base de datos por su ID.
    2. Si no se encuentra, se lanza una excepción 404.
    3. Si el curso existe, se elimina de la base de datos.
    4. Se publica un mensaje en RabbitMQ indicando que el curso fue eliminado.
    """
    db_course = db.query(coursesModel.Course).filter(coursesModel.Course.id == id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    publishDeletedCourse(channel=channel,course_id=db_course.id)
    db_course.is_deleted = True
    db.commit()
    db.refresh(db_course)
    
    return db_course
