from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .user import User
from .base import Base

class Gizi(Base):
    __tablename__ = "gizi"
    
    id = Column(Integer, primary_key=True, index=True)
    nik = Column(String, ForeignKey("users.nik"), index=True)
    bmi = Column(Float)
    status_bmi = Column(String)
    kalori_harian = Column(Integer)

    user = relationship(User, back_populates="gizi")

