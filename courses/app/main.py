from fastapi import FastAPI
from .database.db import engine
from .models import coursesModel, parallelsModel 
from .routes import coursesRout 
from .rabbit.rabbitPublisher import create_rabbit_connection, close_rabbit_connection 

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_rabbit_connection()

@app.on_event("shutdown")
async def shutdown_event():
    close_rabbit_connection()

coursesModel.Base.metadata.create_all(bind=engine)
parallelsModel.Base.metadata.create_all(bind=engine)

app.include_router(coursesRout.router)
