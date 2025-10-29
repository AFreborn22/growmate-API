from sqlalchemy import Column, Integer, String, Float, Date, Enum
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum as pyEnum

class statusEnum(pyEnum) :
    trisemester1 = "trisemester1"
    trisemester2 = "trisemester2"
    trisemester3 = "trisemester3"
    postsemester = "postsemester"

class PAL(pyEnum):
    sedentary = "sedentary"         
    lightly_active = "lightly_active"   
    moderately_active = "moderately_active" 
    very_active = "very_active"      
    super_active = "super_active" 

class User(Base):
    __tablename__ = "users"
    
    nik = Column(String, primary_key=True, index=True)
    nama = Column(String, unique=True, index=True)
    usia = Column(Integer)
    tempat_lahir = Column(String)
    tanggal_lahir = Column(Date)
    tanggal_kehamilan_pertama = Column(Date)
    pal = Column(Enum(PAL))
    alamat = Column(String)
    email = Column(String)
    berat_badan = Column(Float)
    tinggi_badan = Column(Float)
    lingkar_lengan_atas = Column(Float)
    periode_kehamilan = Column(Enum(statusEnum))
    password = Column(String)

gizi = relationship("Gizi", back_populates="user", uselist=False)