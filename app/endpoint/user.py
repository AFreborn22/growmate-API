from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import getDB
from app.models.user import User

router = APIRouter()

@router.get("/me")
def get_user_details(db: Session = Depends(getDB)):

    return {"user": "current user details here"}