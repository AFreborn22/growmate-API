from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from enum import Enum

class statusEnum(str, Enum) :
    trisemester1 = "trisemester1"
    trisemester2 = "trisemester2"
    trisemester3 = "trisemester3"
    postsemester = "postsemester"

class PAL(str, Enum):
    sedentary = "sedentary"         
    lightly_active = "lightly_active"   
    moderately_active = "moderately_active" 
    very_active = "very_active"      
    super_active = "super_active"

class UserSignUp(BaseModel):
    nik: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: date
    tanggal_kehamilan_pertama: date
    pal: str
    alamat: str
    email: EmailStr  
    berat_badan: float
    tinggi_badan: float
    lingkar_lengan_atas: float
    password: str  

    class Config:
        orm_mode = True

class UserSignUpResponse(BaseModel):
    message: str  = "User successfully registered"
    data : dict = {
        "nik": "123456789",
        "nama": "Elizabeth Huang",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "1990-05-15",
        "tanggal_kehamilan_pertama": "2025-06-01",
        "pal": "lightly_active",
        "usia": 35,
        "periode_kehamilan": "trisemester2",
        "alamat": "Jl. Merdeka No.1, Jakarta",
        "email": "elizabeth@example.com",
        "berat_badan": 70.5,
        "tinggi_badan": 170,
        "lingkar_lengan_atas": 25.5,
        "password": "$2b$12$bt06VmHJzC1dwjJEwSGWUeUs/HjDkp10Zv4fAtTe3.mcI.RZHYQ0m"
    }

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkiLCJlbWFpbCI6ImVsaXphYmV0aEBleGFtcGxlLmNvbSIsImV4cCI6MTc2MDYyNjA3OX0.bk9ESkU9fb-p--eFLHAZWX79bheDOScTp-stCRs1buY"
    token_type: str = "bearer"
        
class UserData(BaseModel):
    data : dict = {
        "nik": "123456789",
        "nama": "Elizabeth Huang",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "1990-05-15",
        "tanggal_kehamilan_pertama": "2025-06-01",
        "pal": "lightly_active",
        "usia": 35,
        "periode_kehamilan": "trisemester2",
        "alamat": "Jl. Merdeka No.1, Jakarta",
        "email": "elizabeth@example.com",
        "berat_badan": 70.5,
        "tinggi_badan": 170,
        "lingkar_lengan_atas": 25.5
    }

class UserUpdate(BaseModel):
    nama: Optional[str] | None = None
    tempat_lahir: Optional[str] | None = None
    tanggal_lahir: Optional[date] | None = None
    tanggal_kehamilan_pertama: Optional[date] | None = None
    pal: Optional[str] | None = None
    alamat: Optional[str] | None = None
    email: Optional[EmailStr] | None = None  
    berat_badan: Optional[float] | None = None
    tinggi_badan: Optional[float] | None = None
    lingkar_lengan_atas: Optional[float] | None = None

class UserUpdateResponse(BaseModel):
    message: str = "User Succesfully Updated"
    data : dict = {
        "nama": "Elizabeth Huang",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "1990-05-15",
        "tanggal_kehamilan_pertama": "2025-06-01",
        "pal": "lightly_active",
        "usia": 35,
        "periode_kehamilan": "trisemester2",
        "alamat": "Jl. Merdeka No.1, Jakarta",
        "email": "elizabeth@example.com",
        "berat_badan": 70.5,
        "tinggi_badan": 170,
        "lingkar_lengan_atas": 25.5
    }

    class Config:
        orm_mode = True

#ERROR HANDLING

# Error untuk 400 Bad Request
class BadRequestError(BaseModel):
    detail: str = "Bad Request"
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Bad request, invalid input data."
            }
        }

# Error untuk 404 Not Found
class NotFoundError(BaseModel):
    detail: str = "Resource not found"
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "The requested resource was not found."
            }
        }

# Error untuk 401 Unauthorized
class UnauthorizedError(BaseModel):
    detail: str = "Unauthorized access"
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Unauthorized access. Token may be invalid or missing."
            }
        }

# Error untuk 500 Internal Server Error
class InternalServerError(BaseModel):
    detail: str = "Internal Server Error. An unexpected error occurred."
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "An unexpected error occurred in the server."
            }
        }