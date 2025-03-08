import os
from src.brain import Brain
from src.utils.dbmodels import SessionLocal, User, init_db
from src.utils.security import hash_password, verify_password

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv() # load environment variables from .env file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend's URL if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)

# Initialize the database on startup
@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_username and admin_password:
        existing_user = db.query(User).filter(User.username == admin_username).first()
        if not existing_user:
            admin_user = User(
                username=admin_username,
                hashed_password=hash_password(admin_password)
            )
            db.add(admin_user)
            db.commit()
    db.close()
    
brain = Brain()  # our central processing unit

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    user_text = message.text
    result = brain.handle_message(user_text)
    return result


# Dummy in-memory user store
users_db = {}

class UserSchema(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UserSchema):
    db = SessionLocal()
    if db.query(User).filter(User.username == user.username).first():
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.close()
    return {"username": user.username, "msg": "User registered successfully"}

@app.post("/login")
async def login(user: UserSchema):
    db = SessionLocal()
    stored_user = db.query(User).filter(User.username == user.username).first()
    db.close()
    if not stored_user or not verify_password(user.password, stored_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"msg": "Login successful"}
