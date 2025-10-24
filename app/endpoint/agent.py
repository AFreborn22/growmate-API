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

async def getAgent(query: str, nik: str, token: str):
    url = os.getenv("AGENT", "http://127.0.0.1:8000/api/chat")

    if not url :
        raise ValueError("tidak di temukan di env variable")
    payload = {"query": query,
               "nik" : nik,
               "token" : token}  
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)  
            response.raise_for_status()  
            return response.json()  
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Error during query to RAG agent {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed to RAG agent {str(e)}")

@router.post("/chat", response_model=ChatResponse, responses = chat)
async def chatAgent(query: ChatRequest, db: Session = Depends(getDB), currentUser = Depends(getCurrentUser), token:str =  Depends(getRawToken)):
    try:
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()  
        if not dbUser:
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        
        query = query.query
        chat = await getAgent(
            query=query,
            nik = dbUser.nik,
            token=token
            )  
        return chat  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")