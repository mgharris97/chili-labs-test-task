from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from app.database import Base, engine, SessionLocal
from app.models import User
from app.schemas import RegisterSchema
from app.auth import hash_password
from app.utils import jsend_success, jsend_fail
from pydantic import BaseModel
from fastapi import FastAPI
from app.database import engine, Base


app = FastAPI(title="Chili labs Backend Task")

def get_db():
    # create a new database session (see database.py for SessionMaker)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#make a table on startup
Base.metadata.create_all(bind=engine)

# Endpoints
# Register a user, Login a user, Upload avatar, Open WebSocket, avatar changing notification, Delete user
# HTTP methods POST(create), GET (retrieve/read), DELETE(remove), PUT(replace entirely), PATCH(update partially), WS(real time communication)
# Once I have a better understanding of this, I will implement routes for better organization 


# register user
@app.post('/register')
# pydantic model as method param
def register_user(data: RegisterSchema, db: Session = Depends(get_db)):

    # check to see if the id already exists in the databse
    existing = db.query(User).filter(User.identifier == data.identifier).first()
    if existing:
        raise HTTPException (
            status_code= 400,
            detail= "Identifier already exists"
        )
    
    # Hash password
    hashed = hash_password(data.password)

    # Create a user that becomes a row in the database
    new_user = User(
        identifier = data.identifier,
        password_hash = hashed,
        avatar_url = None,
        id_deleted = False
    )

    # save user to database
    db.add(new_user)
    db.commit
    db.refresh(new_user)

    # create a new JWT token
    playload = {
        "sub": new_user.identifier,
        "exp": datetime.now() + timedelta(hours = 1)
    }
    token = jwt.encode(playload, "SECRET_KEY", algorithm="HS256")

    # Return JSend success response (defined in utils.py)
    return jsend_success({
        "token": token,
        "identifier": new_user.identifier
    })

    

# create a new token
@app.post('/login')
def login_user():
    pass

# Avatar upload 
@app.post('/avatar')
def upload_avatar():
    pass

# Avatar change notification
@app.websocket('/ws/avatar')
def change_avatar():
    pass

# Delete user
@app.delete('/user')
def delete_user():
    pass

# Health
@app.get('/health')
def health():
    pass









