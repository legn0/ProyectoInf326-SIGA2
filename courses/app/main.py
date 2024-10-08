from fastapi import FastAPI
from .database.db import engine
from .models import coursesModel, parallelsModel 
from .routes import coursesRout, parallelsRout 

app = FastAPI()

coursesModel.Base.metadata.create_all(bind=engine)
parallelsModel.Base.metadata.create_all(bind=engine)

app.include_router(coursesRout.router)
app.include_router(parallelsRout.router)