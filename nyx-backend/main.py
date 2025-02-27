from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from brain import Brain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend's URL if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)

brain = Brain()  # our central processing unit

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    user_text = message.text
    result = brain.handle_message(user_text)
    return result
