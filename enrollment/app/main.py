from fastapi import FastAPI
from .api.routes import router as enrollment_router
from .database.database import engine
from .models.models import Base  # Asegúrate de importar Base

# Crear las tablas en la base de datos
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)  # Usa Base aquí
        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

create_tables()

app = FastAPI()
app.include_router(enrollment_router)