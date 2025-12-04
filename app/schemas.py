from pydantic import BaseModel
# Pydantic to enforce types for validation
from sqlalchemy import Column, Integer, String

# Schemas for data
# inherit from BaseModel
# BaseModel 

class RegisterSchema(BaseModel):
    # Pyadntic type hints that look like typical Python type hints, but turn into a validators at runtime
    identifier: str
    password: str

class LoginSchema(BaseModel):
    identifier: str
    password: str 








 