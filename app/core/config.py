import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/growmate")
    SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()