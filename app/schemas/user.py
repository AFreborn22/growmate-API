from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nik: str
    nama: str
    usia: int
    tempat_lahir: str
    tanggal_lahir: str
    alamat: str
    email: EmailStr
    berat_badan: float
    tinggi_badan: float
    lingkar_tangan: float
    password: str

    class Config:
        orm_mode = True


class UserCreateResponse(BaseModel):
    user_data: UserCreate
    message: str


class UserInDB(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nama: Optional[str] = None
    usia: Optional[int] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[str] = None
    alamat: Optional[str] = None
    email: Optional[EmailStr] = None
    berat_badan: Optional[float] = None
    tinggi_badan: Optional[float] = None
    lingkar_tangan: Optional[float] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
