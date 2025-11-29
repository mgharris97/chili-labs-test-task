from pydantic import BaseModel
from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(title="Chili labs Backend Task")

#make a table on startup
Base.metadata.create_all(bind=engine)

# GET, PUT, POST, DELETE

@app.get('/')
def health_check():
    return {"status": "Success", "data": "API is running!"}




