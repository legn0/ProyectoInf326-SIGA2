from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.db import get_db 
from ..models import parallelsModel
from ..schemas import parallelsSchemas 

router = APIRouter(
    prefix="/parallels",
    tags=["Parallels"]
)
