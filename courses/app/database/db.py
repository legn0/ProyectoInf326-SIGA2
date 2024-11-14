from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE = os.getenv("SQLALCHEMY_DATABASE_URL")
SQL_DB = os.getenv("MYSQL_DATABASE")
SQL_USR = os.getenv("MYSQL_USER")
SQL_PWRD = os.getenv("MYSQL_PASSWORD")
SQL_PORT = os.getenv("MYSQL_PORT")

SQL_URL = f"mysql://{SQL_USR}:{SQL_PWRD}@{SQLALCHEMY_DATABASE}:{SQL_PORT}/{SQL_DB}"

engine = create_engine(SQL_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()