from fastapi import FastAPI
from .database.db import engine
from .models import coursesModel, parallelsModel 
from .routes import coursesRout, parallelsRout
from fastapi.middleware.cors import CORSMiddleware
# from .rabbit.rabbitPublisher import create_rabbit_connection, close_rabbit_connection 

app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     create_rabbit_connection()

# @app.on_event("shutdown")
# async def shutdown_event():
#     close_rabbit_connection()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

coursesModel.Base.metadata.create_all(bind=engine)
parallelsModel.Base.metadata.create_all(bind=engine)

app.include_router(coursesRout.router)
app.include_router(parallelsRout.router)
