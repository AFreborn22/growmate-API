from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.forms import OAuth2PasswordRequestFormCompat
from app.core.security import (createAccessToken, getCurrentUser, hashPassword,
                               verifyPassword)
from app.db.session import getDB
from app.models.user import User
from app.schemas.user import (Token, UserCreate, UserCreateResponse, UserLogin,
                              UserUpdate)

router = APIRouter()


# Endpoint untuk sign-up
@router.post("/signup", response_model=UserCreateResponse)
def signup(user: UserCreate, db: Session = Depends(getDB)):
    try:
        # Cek apakah NIK atau email sudah ada di database
        existing_user_nik = db.query(User).filter(User.nik == user.nik).first()
        existing_user_email = db.query(User).filter(
            User.email == user.email).first()

        if existing_user_nik:
            raise HTTPException(
                status_code=400, detail="NIK already registered")

        if existing_user_email:
            raise HTTPException(
                status_code=400, detail="Email already registered")

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
            # Meng-hash password sebelum disimpan
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
        # Menangani error integritas (misalnya NIK atau email yang sudah ada)
        db.rollback()
        raise HTTPException(status_code=400, detail="Data integrity error")
    except Exception as e:
        # Menangani kesalahan umum lainnya
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your request: {str(e)}")  # noqa


# Endpoint untuk login
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestFormCompat = Depends(), db: Session = Depends(getDB)):
    db_user = db.query(User).filter(User.email == form.email).first()
    if not db_user or not verifyPassword(form.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access_token = createAccessToken(
        data={"sub": db_user.nik, "email": db_user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint untuk update user
@router.put("/update")
def update_user(user: UserUpdate, db: Session = Depends(getDB), currentUser=Depends(getCurrentUser)):
    try:
        # Cari user berdasarkan NIK yang terautentikasi
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()
        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")

        # Update data sesuai dengan yang dikirimkan dalam request
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

        return {"message": "Update data successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")  # noqa
