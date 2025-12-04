from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.database import Base, engine, SessionLocal
from app.models import User
from app.schemas import RegisterSchema
from app.auth import hash_password
from app.utils import jsend_success, jsend_fail
from pydantic import BaseModel
from fastapi import FastAPI
from app.database import engine, Base
from app.auth import hash_password, verify_password
from app.schemas import LoginSchema, RegisterSchema
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Chili labs Backend Task")

def make_jwt(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    payload = {
        "sub": subject,
        "exp": expire
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

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

    token = make_jwt(new_user.identifier)
    # Return JSend success response (defined in utils.py)
    return jsend_success({
        "token": token,
        "identifier": new_user.identifier
    })

    #************************************
    # end of /register endpoint
    #************************************


# create a new token
@app.post('/login')
def login_user(data: LoginSchema, db: Session = Depends(get_db)):
    # user present in db
    user_existing = db.query(User).filter(User.identifier == data.identifier).first()
    
    #Check if user is not inside the db
    if not user_existing:
        raise HTTPException(
            status_code= 400,
            detail='User Does not exist'
        )
    if user_existing.is_deleted:
        raise HTTPException(
            status_code=401,
            detail='Authentication failed'
        )
 
    if not verify_password(data.password, user_existing.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid identifier or password"
    )

    # Assing a JWT to user_existing
    jwt_token = make_jwt(user_existing.identifier)

    return jsend_success({
        "token": jwt_token,
        "identifier": user_existing.identifier
    })


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









