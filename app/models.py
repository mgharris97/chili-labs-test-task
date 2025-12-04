from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# Table called 'users' in the database 
# Each row in users db has following columns: id, identifier, password_hash, avatar_url, and is_deleted
class User(Base):
    __tablename__ = 'users'
    # internal primary key
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False) 
