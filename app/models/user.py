from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    nik = Column(String, primary_key=True, index=True)
    nama = Column(String, unique=True, index=True)
    usia = Column(Integer)
    tempat_lahir = Column(Date)
    tanggal_lahir = Column(String)
    alamat = Column(String)
    email = Column(String)
    berat_badan = Column(Float)
    tinggi_badan = Column(Float)
    lingkar_tangan = Column(Float)
    password = Column(String)

gizi = relationship("Gizi", back_populates="user", uselist=False)