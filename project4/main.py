import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Message(BaseModel):
    query: str


app = FastAPI()

load_dotenv(".env")

def get_current_temperature(location: str) -> dict:
    return {"location": location, "temperature": 32, "unit": "Celsius", "condition": "Sunny"}  

weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

api_key = os.getenv("Gemini_API_Key")
if not api_key:
    raise ValueError("Gemini_API_Key is missing from .env")


client = genai.Client(api_key=api_key)
@app.post("/ai-query")
async def generate_response(message:Message):
    try:
        config=types.GenerateContentConfig(tools=[types.Tool(function_declarations=[weather_function])])
        
        response=await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=message.query,
            config=config
            )
        if not response.function_calls: 
            return {"answer": response.text}
        
        call = response.function_calls[0]
        result = get_current_temperature(**call.args)

        second_response = await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=message.query)]),
                response.candidates[0].content,
                types.Content(role="user", parts=[
                    types.Part.from_function_response(name=call.name, response={"result": result})
                ]),
            ],
            config=config
        )
        return {"answer": second_response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
