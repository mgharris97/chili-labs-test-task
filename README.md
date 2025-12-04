## ChiliLabs Backend Task Using FastAPI

This project implements the Chili Labs Backend Task found [here](https://github.com/ChiliLabs/test-tasks/blob/master/backend_developer.md) 

My personal reflection can be found at the [bottom](https://github.com/mgharris97/chili-labs-test-task/edit/main/README.md#personal-reflection)

---

## Tech Stack
- FastAPI
- SQLite
- SQAlchemy
- Pydantic
- python-jose for JWT
- Passlib

## Features
Authentication 
- Stateless JWT authentication
- Tokens issued on /login and /register
- Token validation

User Operation
- Register a new user
- Login with identifier and passowrd
- Upload an avatar that is saved as identifier.png in Avatars folder
- WebSocket for notification of avatar chnage
- /delete provides ability to remove a user and their avatar from the database

Other
- JSend success / error responses
- Automatic database creation
- Organized FastAPI structure using schemas for input validation, model for database entries

## Project Structure
```md
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── auth.py          # Password hashing and verification
│   ├── database.py      # SQLAlchemy engine and SessionLocal
│   ├── main.py          # All endpoints register, login, avatar, WebSocket, delete
│   ├── models.py        # User model definition
│   ├── schemas.py       # Request validation
│   └── utils.py         # JSend response helpers
├── app.db 
├── avatars              # Saved images
├── README.md
├── requirements.txt
└── .env                 # SECRET_KEY 
```

## Environment setup
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Create a .env file in project root
```bash
SECRET_KEY=your_secret_key_here
```
3. Run the server
```bash
fastapi dev main.py
```
4. Backend runs on
```bash
http://localhost:8000
```
5. With interactive API docs at
```bash
http://localhost:8000/docs
```

## API Endpoints, their HTTP methods, purpose, body/schema
**POST /register**
  
  - Register a new user
  
Body:
```json
{
  "identifier": "example@email.com",
  "password": "yourpassword"
}
```
Returns:
```json
{
  "status": "success",
  "data": {
    "token": "...",
    "identifier": "..."
  }
}
```

**POST /login**
  - Get a JSON Web Token

**POST /avatar (requires auth)**
  - Upload an avatar

Header:
```python
Authorization: Bearer <token>
```

**WS /ws/avatar (requires Auth)**
- Receives notifications when the user’s avatar updates

Clinet must send token in header 
```python
token: <jwt>
```

**DELETE /user (requires Auth)**
- Marks user as deleted, removes avatar, prevents reuse of past tokens.
**GET /health**
- Simple health check.
## Database
- SQLite is used by default
- Tables auto create on startup
```python
Base.metadata.create_all(bind=engine)
```

# Personal reflection

When I first read through the requirements of this task, I must admit I was taken aback. I had no idea what 80% of the terms meant and required as this task was simply beyond the scope of my current understanding. I had no idea how to make a backend, hell, what the backend even meant, what an endpoint was, the different toolkits used to make such things, e.g. Django, Flash, FastAPI. I had never heard of SQAlchemy and had barely any previous experience with databases let alone JSON Web Tokens. I was disheartened and felt beat by what you consider a simple project. I don't doubt that sentiment, but for me, it felt massive and complex. That said, I still decided to give it a try with all of the resources available out there; Google, LLMs, Reddit, Stack Overflow, official documentation, and tutorial pages. Little by little, I managed create a rough structure of the project and gain a better understanding of the abstract nature of the backend. Little by little, I learned what a JWT is, how to implement it and verify it, what a salt is, what password hashing is and how it is done / why it is done. I learned how to manage a database using SQAlchemy and why certain code is segmented in multiple files, even if containing only a few lines instead of crowding main.py. Sure, it's a basic understanding barely scratching the surface the backend development, but it's the spark I needed to gain interest and motivation to continue in this project and beyond. So even if I am underqualified for this position, I am immensely grateful for the lessons learned in the past week.

Thank you,

Matthew Harris




