import asyncio
from fastapi import FastAPI
from .api.routes import router as enrollment_router
from .database.database import engine
from .models.models import Base 
from .rabbit_consume.course_consume import consume_rabbitmq_messages
def create_tables():
    try:
        Base.metadata.create_all(bind=engine) 
        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

create_tables()
app = FastAPI()
app.include_router(enrollment_router)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(start_rabbitmq_consumer())

async def start_rabbitmq_consumer():
    await asyncio.to_thread(consume_rabbitmq_messages)
