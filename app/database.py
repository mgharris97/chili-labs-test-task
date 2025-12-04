from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Using SQLAlchemy to access and work with SQL database while using Python syntax since my SQL syntax is very limited
#SQLite database URL

DATABASE_URL = 'sqlite:///./app.db'
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}) # Only the thread that opened the SQLite connection is allowed to use it.

# Create a new database session factory when called
# later when called db = SessionLocal, db becomes a new session
# Every API request gets its own session
SessionLocal = sessionmaker(
    autocommit=False, #must explicitly call commit when making a new session 
    autoflush=False,
    bind=engine #Session is connected to SQLite database
)
 
Base = declarative_base()
