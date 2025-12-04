from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.database import Base, engine, SessionLocal
from app.models import User
from app.schemas import RegisterSchema, LoginSchema
from app.auth import hash_password
from app.utils import jsend_success
from app.auth import verify_password
from dotenv import load_dotenv
bearer_scheme = HTTPBearer()
load_dotenv()
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Chili labs Backend Task")


def make_jwt(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Decode the token and get user identifier
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        return None


def get_db():
    # create a new database session (see database.py for SessionMaker)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# make a table on startup
Base.metadata.create_all(bind=engine)

# Endpoints
# Register a user, Login a user, Upload avatar, Open WebSocket, avatar changing notification, Delete user
# HTTP methods POST(create), GET (retrieve/read), DELETE(remove), PUT(replace entirely), PATCH(update partially), WS(real time communication)
# Once I have a better understanding of this, I will implement routes for better organization


# register user
@app.post("/register")
# pydantic model as method param
def register_user(data: RegisterSchema, db: Session = Depends(get_db)):
    # check to see if the id already exists in the databse
    existing = db.query(User).filter(User.identifier == data.identifier).first()
    if existing:
        raise HTTPException(status_code=400, detail="Identifier already exists")

    # Hash password
    hashed = hash_password(data.password)

    # Create a user that becomes a row in the database
    new_user = User(
        identifier=data.identifier,
        password_hash=hashed,
        avatar_url=None,
        is_deleted=False,
    )

    # save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = make_jwt(new_user.identifier)
    # Return JSend success response (defined in utils.py)
    return jsend_success({"token": token, "identifier": new_user.identifier})

    # ************************************
    # end of /register endpoint
    # ************************************


# create a new token
@app.post("/login")
def login_user(data: LoginSchema, db: Session = Depends(get_db)):
    # user present in db
    user_existing = db.query(User).filter(User.identifier == data.identifier).first()

    # Check if user is not inside the db
    if not user_existing:
        raise HTTPException(status_code=400, detail="User Does not exist")
    if user_existing.is_deleted:
        raise HTTPException(status_code=401, detail="Authentication failed")

    if not verify_password(data.password, user_existing.password_hash):
        raise HTTPException(status_code=401, detail="Invalid identifier or password")

    # Assing a JWT to user_existing
    jwt_token = make_jwt(user_existing.identifier)

    return jsend_success({"token": jwt_token, "identifier": user_existing.identifier})


# Avatar upload
# def "Stand in line and wait your turn"
# async def "Take a number, do other tings, get notified when ready"
@app.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    token: str = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # handle invalid/expired token
    identifier = decode_token(token.credentials)
    if not identifier:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # verify the user exists
    # looks up the user in the database by identifier extracted from the JWT.
    user = db.query(User).filter(User.identifier == identifier).first()
    # reject deleted or missing users
    if not user or user.is_deleted:
        raise HTTPException(status_code=401, detail="User not authorized")

    # folder for pictures
    folder = "avatars"
    # exist_ok=True prevents errors if the folder already exists
    os.makedirs(folder, exist_ok=True)
    # name of avatar
    file_path = os.path.join(folder, f"{identifier}.png")

    # save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    user.avatar_url = file_path
    db.commit()
    db.refresh(user)

    return jsend_success({"avatar_url": file_path})


# Avatar change notificatio
@app.websocket("/ws/avatar")
def change_avatar():
    pass


# Delete user
@app.delete("/user")
def delete_user(token: str = Depends(bearer_scheme), db: Session = Depends(get_db)):
    # handle invalid/expired token like /avatar
    identifier = decode_token(token.credentials)
    if not identifier:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # look up the user in db
    user = db.query(User).filter(User.identifier == identifier).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if the user is deleted, raise an exception 
    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User already deleted")

    # make user_deleted to true
    user.is_deleted = True

    # if the user has an avatar remove it
    if user.avatar_url and os.path.exists(user.avatar_url):
        os.remove(user.avatar_url)
        user.avatar_url = None

    # update the databse
    db.commit()
    db.refresh(user)

    # jsend success message
    return jsend_success({"message": "User deleted successfully"})


# Health
# Health
@app.get("/health")
def health():
    return jsend_success({"message": "API is running. 123"}) 
