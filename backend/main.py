from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

app = FastAPI()

# OpenAI API anahtarını al
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# İstek gövdesi (Body) için bir model oluştur
class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat/")
async def chat_with_ai(request: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="API key is missing.")
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": request.prompt}],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL, json=data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()
