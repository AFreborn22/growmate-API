from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/growmate")  # noqa
    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://:@localhost:5432/growmate")  # noqa
    SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
