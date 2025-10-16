from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserUpdate, UserLogin, UserData, UserUpdateResponse, Token, HTTPError
from app.resExample.auth import signup, login, getData, updateData
from app.db.session import getDB
from app.models.user import User
from app.core.security import createAccessToken, verifyPassword, hashPassword, getCurrentUser
from app.helper.ageCount import ageCount
from app.helper.pregnantCount import trisemesterCount

router = APIRouter()

# Endpoint untuk sign-up
@router.post("/signup", response_model=UserCreate, responses=signup)
def signup(user: UserCreate, db: Session = Depends(getDB)):
    try:
        # Cek apakah NIK atau email sudah ada di database
        existing_user_nik = db.query(User).filter(User.nik == user.nik).first()
        existing_user_email = db.query(User).filter(User.email == user.email).first()

        if existing_user_nik:
            raise HTTPException(status_code=400, detail="NIK already registered")
        
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        usia = ageCount(user.tanggal_lahir)
        periode_kehamilan = trisemesterCount(user.tanggal_kehamilan_pertama)
        
        # Membuat data user untuk disimpan ke database
        user_data = {
            "nik": user.nik,
            "nama": user.nama,
            "tempat_lahir": user.tempat_lahir,
            "tanggal_lahir": user.tanggal_lahir,
            "tanggal_kehamilan_pertama": user.tanggal_kehamilan_pertama,
            "pal": user.pal,
            "usia": usia,
            "periode_kehamilan": periode_kehamilan,
            "alamat": user.alamat,
            "email": user.email,
            "berat_badan": user.berat_badan,
            "tinggi_badan": user.tinggi_badan,
            "lingkar_lengan_atas": user.lingkar_lengan_atas,
            "password": hashPassword(user.password)  
        }

        print(user_data)

        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

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
@router.post("/login", response_model=Token, responses=login)
def login(user: UserLogin, db: Session = Depends(getDB)):
    dbUser = db.query(User).filter(User.email == user.email).first()
    if not dbUser or not verifyPassword(user.password, dbUser.password):
        raise HTTPException(status_code=400, detail="Incorrect Email or Password")

    access_token = createAccessToken(data={"sub": dbUser.nik, "email": dbUser.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/data", response_model=UserData, responses=getData)
def getData(db: Session = Depends(getDB), currentUser = Depends(getCurrentUser)):
    try :
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()
        if not dbUser:
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        
        return dbUser 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")


# Endpoint untuk update user
@router.put("/update", response_model=UserUpdateResponse, responses=updateData)
def update_user(user: UserUpdate, db: Session = Depends(getDB), currentUser = Depends(getCurrentUser)):
    try:
        # Find user in database
        dbUser = db.query(User).filter(User.nik == currentUser.nik).first()
        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")

        updated = False
        updatedField = {}

        # Check and update user fields only if changed
        if user.nama and user.nama != dbUser.nama:
            dbUser.nama = user.nama
            updatedField["nama"] = dbUser.nama
            updated = True
        if user.tempat_lahir and user.tempat_lahir != dbUser.tempat_lahir:
            dbUser.tempat_lahir = user.tempat_lahir
            updatedField["tempat_lahir"] = dbUser.tempat_lahir
            updated = True
        if user.tanggal_lahir and user.tanggal_lahir != dbUser.tanggal_lahir:
            dbUser.tanggal_lahir = user.tanggal_lahir
            dbUser.usia = ageCount(dbUser.tanggal_lahir)
            updatedField["tanggal_lahir"] = dbUser.tanggal_lahir
            updatedField["usia"] = dbUser.usia
            updated = True
        if user.tanggal_kehamilan_pertama and user.tanggal_kehamilan_pertama != dbUser.tanggal_kehamilan_pertama:
            dbUser.tanggal_kehamilan_pertama = user.tanggal_kehamilan_pertama
            dbUser.periode_kehamilan = trisemesterCount(dbUser.tanggal_kehamilan_pertama)
            updatedField["tanggal_kehamilan_pertama"] = dbUser.tanggal_kehamilan_pertama
            updatedField["periode_kehamilan"] = dbUser.periode_kehamilan
            updated = True
        if user.pal and user.pal != dbUser.pal:
            dbUser.pal = user.pal
            updatedField["pal"] = dbUser.pal
            updated = True
        if user.alamat and user.alamat != dbUser.alamat:
            dbUser.alamat = user.alamat
            updatedField["alamat"] = dbUser.alamat
            updated = True
        if user.berat_badan and user.berat_badan != dbUser.berat_badan:
            dbUser.berat_badan = user.berat_badan
            updatedField["berat_badan"] = dbUser.berat_badan
            updated = True
        if user.tinggi_badan and user.tinggi_badan != dbUser.tinggi_badan:
            dbUser.tinggi_badan = user.tinggi_badan
            updatedField["tinggi_badan"] = dbUser.tinggi_badan
            updated = True
        if user.lingkar_lengan_atas and user.lingkar_lengan_atas != dbUser.lingkar_lengan_atas:
            dbUser.lingkar_lengan_atas = user.lingkar_lengan_atas
            updatedField["lingkar_lengan_atas"] = dbUser.lingkar_lengan_atas
            updated = True

        if updated:
            db.commit()
            db.refresh(dbUser)
            responseData = {"message": "Update Successful", "data": updatedField}
        else:
            responseData = {"message": "No changes made", "data": updatedField}

        return responseData

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {str(e)}")