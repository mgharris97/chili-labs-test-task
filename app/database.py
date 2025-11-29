from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#SQLite database URL
#DATABASE_URL = "sqlite:///./app.db"

engine = create_engine('sqlite:///./app.db', connect_args={"check_same_thread": False})

#Session class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
 
Base = declarative_base()
