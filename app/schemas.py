from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

# Schemas for data
# inherit from BaseModel
# BaseModel 

class RegisterSchema(BaseModel):
    identifier: str
    password: str

class LoginSchema(BaseModel):
    identifier: str
    password: str








