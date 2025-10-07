from datetime import datetime, timedelta

# from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import getDB
from app.models.user import User

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
    encodedJWT = jwt.encode(
        toEncode, settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encodedJWT


# Memverifikasi token JWT
def verifyToken(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        # 401 with proper challenge header so Swagger understands it
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
bearer_scheme = HTTPBearer(auto_error=False)


def getCurrentUser(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
    # token: str = Depends(oauth2Scheme),
    db: Session = Depends(getDB)
) -> User:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verifyToken(creds.credentials)
    nik: str | None = payload.get("sub")
    if not nik:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.nik == nik).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
