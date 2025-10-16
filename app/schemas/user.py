from pydantic import BaseModel, EmailStr, Field, root_validator
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

class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Error message"}
        }

class UserCreate(BaseModel):
    nik: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: date
    tanggal_kehamilan_pertama: date
    pal: PAL = Field(default="sedentary", examples=["sedentary", "lightly active", "moderately active" , "very active", "super active"])
    alamat: str
    email: EmailStr  
    berat_badan: float
    tinggi_badan: float
    lingkar_lengan_atas: float
    password: str  

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        
class UserData(BaseModel):
    nik: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: date
    tanggal_kehamilan_pertama: date
    pal: PAL 
    usia: int
    alamat: str
    email: EmailStr  
    berat_badan: float
    tinggi_badan: float
    lingkar_lengan_atas: float
    periode_kehamilan: statusEnum

class UserSignupResponse(BaseModel):
    user_data: UserData = {
        "nik": "123456789",
        "nama": "Elizabeth Huang",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "1990-05-15",
        "tanggal_kehamilan_pertama": "2025-06-01",
        "pal": "lightly active",
        "alamat": "Jl. Merdeka No.1, Jakarta",
        "email": "elizabeth@example.com",
        "berat_badan": 70.5,
        "tinggi_badan": 170.0,
        "lingkar_lengan_atas": 25.5,
    }
    message: str = "User successfully registered."

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    nama: Optional[str] | None = None
    tempat_lahir: Optional[str] | None = None
    tanggal_lahir: Optional[date] | None = None
    tanggal_kehamilan_pertama: Optional[date] | None = None
    pal: Optional[PAL] | None = None
    alamat: Optional[str] | None = None
    email: Optional[EmailStr] | None = None  
    berat_badan: Optional[float] | None = None
    tinggi_badan: Optional[float] | None = None
    lingkar_lengan_atas: Optional[float] | None = None

class UserUpdateResponse(BaseModel):
    message: str
    data : dict

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str