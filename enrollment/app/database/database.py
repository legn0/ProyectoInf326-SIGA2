from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv("DATABASE_URL")
SQL_DB = os.getenv("MYSQL_DATABASE")
SQL_USER = os.getenv("MYSQL_USER")
SQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
SQL_PORT = os.getenv("MYSQL_PORT")
SQL_IP = os.getenv("SQLALCHEMY_DATABASE_URL")

SQL_URL = f"{DATABASE_URL}"

engine = create_engine(SQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()