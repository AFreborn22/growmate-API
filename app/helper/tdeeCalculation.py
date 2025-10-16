from sqlalchemy.orm import Session
from app.models.user import User, statusEnum, PAL
from app.models.gizi import Gizi

def bmiCount(berat_badan, tinggi_badan):
    tinggiOnMeter = tinggi_badan / 100
    bmi = berat_badan / (tinggiOnMeter ** 2)

    return bmi

# BMR menggunakan rumus Mifflin-St Jeor
def bmrCount(berat_badan, tinggi_badan, usia):
    bmr = 10 * berat_badan + 6.25 * tinggi_badan - 5 * usia - 161
    return bmr

def palToNumber(pal):

    if isinstance(pal, PAL):
        pal = pal.value

    if pal == "sedentary" :
        pal = 1.2
    elif pal == "lightly_active" :
        pal = 1.375
    elif pal == "moderately_active" :
        pal = 1.55
    elif pal == "very_active" :
        pal = 1.725
    elif pal == "super_active" :
        pal = 1.9

    return pal

# menghitung TDEE berdasarkan BMR dan tingkat aktivitas fisik (PAL)
def hitungTdee(bmr, pal):
    pal = palToNumber(pal)
    tdee = bmr * pal
    return tdee

# hitung by AKG kemenkes untuk Ibu hamil
def kaloriHarian(berat_badan, tinggi_badan, usia, pal, periode_kehamilan, mode="AKG"):
    bmr = bmrCount(berat_badan, tinggi_badan, usia)
    tdee = hitungTdee(bmr, pal)

    if isinstance(periode_kehamilan, statusEnum):
        periode_kehamilan = periode_kehamilan.value

    if mode == "AKG" :
        if periode_kehamilan == "trisemester1" :
            kalori_harian = tdee + 180
        elif periode_kehamilan == "trisemester2" or periode_kehamilan =="trisemester3" :
            kalori_harian = tdee + 300

    else :
        if periode_kehamilan == "trisemester2" :
            kalori_harian = tdee + 340
        if periode_kehamilan == "trisemester3" :
            kalori_harian = tdee + 450
        else :
            kalori_harian = tdee
    
    return kalori_harian

def updateGizi(nik: str, berat_badan: float, tinggi_badan: float, usia: int, pal: str, periode_kehamilan: str, db: Session):

    # Ambil data user by NIK
    user = db.query(User).filter(User.nik == nik).first()
    
    if not user:
        return {"message": "User not found"}
    
    if tinggi_badan <= 0:
        return {"message": "Tinggi badan tidak valid"}
    
    # Hitung BMI
    bmi = bmiCount(berat_badan, tinggi_badan)
    
    # Tentukan status BMI
    if bmi < 18.5:
        status_bmi = "Kekurangan Berat Badan"
    elif 18.5 <= bmi < 24.9:
        status_bmi = "Normal"
    elif 25 <= bmi < 29.9:
        status_bmi = "Kelebihan Berat Badan"
    else:
        status_bmi = "Obesitas"


    try :
        
        kalori_harian = kaloriHarian(berat_badan, tinggi_badan, usia, pal, periode_kehamilan, mode="AKG")  
        print(kalori_harian)

    except Exception as e:
        print(f"Error in calculating kalori_harian: {str(e)}")  
        return {"message": f"Error in calculating kalori_harian: {str(e)}"}

    gizi = db.query(Gizi).filter(Gizi.nik == nik).first()
    
    if not gizi:
        gizi = Gizi(nik=nik, bmi=bmi, status_bmi=status_bmi, kalori_harian=kalori_harian)
        db.add(gizi)
    else:
        gizi.bmi = bmi
        gizi.status_bmi = status_bmi
        gizi.kalori_harian = kalori_harian

    db.commit()
    db.refresh(gizi)
    
    return {
        "message": f"Data updated successfully for user {nik}",
        "data": {  
            "bmi": bmi,
            "status_bmi": status_bmi,
            "kalori_harian": kalori_harian
        }
    }