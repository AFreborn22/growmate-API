import httpx
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException   
from sqlalchemy.orm import Session
from app.db.session import getDB
from app.models.user import User
from app.core.security import getCurrentUser, getRawToken
from app.schemas.agent import ChatRequest, ChatResponse
from app.resExample.agent import chat

router = APIRouter()
load_dotenv() 

TIMEOUT = 15.0 
AGENT_URL = os.getenv("AGENT", "http://127.0.0.1:8000/api/chat")

@router.post("/chat", response_model=ChatResponse, responses=chat)
async def chatAgent(
    query: ChatRequest, 
    db: Session = Depends(getDB), 
    currentUser: User = Depends(getCurrentUser), 
    token: str = Depends(getRawToken),
):
    try:
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()  
        if not dbUser:
            raise HTTPException(status_code=404, detail="Invalid Credentials")

        payload = {
            "query": query.query,
            "nik": dbUser.nik,
            "token": token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AGENT_URL, 
                json=payload, 
                timeout=TIMEOUT 
            )  
            response.raise_for_status()  
            return response.json() 

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code if e.response is not None else 500
        detail = f"RAG Agent returned an error: {e.response.text if e.response else str(e)}"
        raise HTTPException(status_code=status_code, detail=detail)
        
    except httpx.RequestError as e:
        raise HTTPException(status_code=504, detail=f"RAG Agent request failed (Timeout/Connection Error): {str(e)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")