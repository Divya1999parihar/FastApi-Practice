import os
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Message(BaseModel):
    query: str


app = FastAPI()


load_dotenv(".env")

api_key = os.getenv("Gemini_API_Key")
if not api_key:
    raise ValueError("Gemini_API_Key is missing from .env")

client = genai.Client(api_key=api_key)
@app.post("/ai-query")
def generate_response(message:Message):
    try:
        response=client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message.query,
            
    ) 
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
