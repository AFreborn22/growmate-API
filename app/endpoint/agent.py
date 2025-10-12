import httpx
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import getDB
from app.models.user import User
from app.core.security import getCurrentUser
from app.schemas.agent import ChatRequest

router = APIRouter()

async def getAgent(query: str):
    url = "http://127.0.0.1:8000/api/agent/chat"  
    payload = {"query": query}  
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)  
            response.raise_for_status()  
            return response.json()  
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail="Error during query to RAG agent")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Request failed to RAG agent")

@router.post("/chat")
async def chatAgent(query: ChatRequest, db: Session = Depends(getDB), currentUser = Depends(getCurrentUser)):
    try:
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()  
        if not dbUser:
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        
        chat = await getAgent(query)  
        return chat  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")