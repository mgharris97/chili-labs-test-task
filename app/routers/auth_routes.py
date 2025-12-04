# routes specifically for authentication routes

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import RegisterSchema
from app.utils import jsend_success, jsend_fail
from app.auth import hash_password


router = APIRouter(prefix="/auth")
    