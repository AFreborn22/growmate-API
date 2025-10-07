from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nik = Column(String, unique=True, index=True)
    nama = Column(String, unique=True, index=True)
    usia = Column(Integer)
    tempat_lahir = Column(String)
    tanggal_lahir = Column(String)
    alamat = Column(String)
    email = Column(String)
    berat_badan = Column(Float)
    tinggi_badan = Column(Float)
    lingkar_tangan = Column(Float)
    password = Column(String)