from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

#Table for registration

id = Column(Integer, primary_key=True, index=True)
identifier = Column(String, unique=True, index=True, nullable=False)
password_hash = Column(String, nullable=False)
avatar_url = Column(String, nullable=True)
is_deleted = Column(Boolean, default=False) 

x