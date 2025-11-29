from pydantic import BaseModel
from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(title="Chili labs Backend Task")

#make a table on startup
Base.metadata.create_all(bind=engine)

# Endpoints
# Register a user, Login a user, Upload avatar, Open WebSocket, avatar changing notification, Delete user
# HTTP methods POST(create), GET (retrieve/read), DELETE(remove), PUT(replace entirely), PATCH(update partially), WS(real time communication)


# register user
@app.post('/register')
def register_user():
    pass

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









