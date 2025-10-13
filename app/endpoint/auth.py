from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserUpdate, UserLogin, Token
from app.db.session import getDB
from app.models.user import User
from app.core.security import createAccessToken, verifyPassword, hashPassword, getCurrentUser

router = APIRouter()

# Endpoint untuk sign-up
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(getDB)):
    try:
        # Cek apakah NIK atau email sudah ada di database
        existing_user_nik = db.query(User).filter(User.nik == user.nik).first()
        existing_user_email = db.query(User).filter(User.email == user.email).first()

        if existing_user_nik:
            raise HTTPException(status_code=400, detail="NIK already registered")
        
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Membuat data user untuk disimpan ke database
        user_data = {
            "nik": user.nik,
            "nama": user.nama,
            "usia": user.usia,
            "tempat_lahir": user.tempat_lahir,
            "tanggal_lahir": user.tanggal_lahir,
            "alamat": user.alamat,
            "email": user.email,
            "berat_badan": user.berat_badan,
            "tinggi_badan": user.tinggi_badan,
            "lingkar_tangan": user.lingkar_tangan,
            "password": hashPassword(user.password)  
        }
        
        # Menyimpan user ke database
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Menyusun response yang berisi data user yang baru dibuat dan pesan sukses
        responseData = {
            "user_data": user_data,
            "message": "User successfully registered"
        }

        return responseData

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Data integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")

# Endpoint untuk login
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(getDB)):
    dbUser = db.query(User).filter(User.email == user.email).first()
    if not dbUser or not verifyPassword(user.password, dbUser.password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = createAccessToken(data={"sub": dbUser.nik, "email": dbUser.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint untuk update user
@router.put("/update")
def update_user(user: UserUpdate, db: Session = Depends(getDB), currentUser = Depends(getCurrentUser)):
    try:

        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()
        if not dbUser:
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        
        if user.nama:
            dbUser.nama = user.nama
        if user.usia:
            dbUser.usia = user.usia
        if user.tempat_lahir:
            dbUser.tempat_lahir = user.tempat_lahir
        if user.tanggal_lahir:
            dbUser.tanggal_lahir = user.tanggal_lahir
        if user.alamat:
            dbUser.alamat = user.alamat
        if user.berat_badan:
            dbUser.berat_badan = user.berat_badan
        if user.tinggi_badan:
            dbUser.tinggi_badan = user.tinggi_badan
        if user.lingkar_tangan:
            dbUser.lingkar_tangan = user.lingkar_tangan

        # Commit perubahan ke database
        db.commit()
        db.refresh(dbUser)

        return {"user": user,
                "message": "Update data successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")