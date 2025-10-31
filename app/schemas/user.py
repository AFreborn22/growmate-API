from pydantic import BaseModel, EmailStr
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
    data : dict

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
        
class UserSchema(BaseModel):
    nik: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: date
    tanggal_kehamilan_pertama: date
    pal: str
    usia: int 
    periode_kehamilan: str 
    alamat: str
    email: EmailStr
    berat_badan: float
    tinggi_badan: float
    lingkar_lengan_atas: float
    
    class Config:
        orm_mode = True 

class UserData(BaseModel):
    data : UserSchema 

    class Config: 
        orm_mode = True

class UserUpdate(BaseModel):
    nama: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    tanggal_kehamilan_pertama: Optional[date] = None
    pal: Optional[str] = None
    alamat: Optional[str] = None
    email: Optional[EmailStr] = None  
    berat_badan: Optional[float] = None
    tinggi_badan: Optional[float] = None
    lingkar_lengan_atas: Optional[float] = None

class UserUpdateResponse(BaseModel):
    message: str 
    data : dict

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