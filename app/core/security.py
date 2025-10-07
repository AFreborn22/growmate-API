from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.session import getDB
from app.core.config import settings


# Pengaturan hashing password
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Membuat hash password
def hashPassword(password: str) -> str:

    password = password.encode('utf-8')
    print(f"Password length: {len(password)} bytes")  
    if len(password) > 72:
        password = password[:72]  
    return pwdContext.hash(password)


# Memverifikasi hash password
def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    return pwdContext.verify(plainPassword, hashedPassword)

# Membuat token akses
def createAccessToken(data: dict) -> str:
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})
    encodedJWT = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encodedJWT

# Memverifikasi token JWT
def verifyToken(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(getDB)) -> User:
    try:
        payload = verifyToken(token)  
        if payload is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        nik: str = payload.get("sub")
        if nik is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        db_user = db.query(User).filter(User.nik == nik).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return db_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")