from sqlalchemy.orm import Session
from app.models.user import User
from app.models.gizi import Gizi


def bmiCount(berat_badan, tinggi_badan):
    tinggiOnMeter = tinggi_badan / 100
    bmi = berat_badan / (tinggiOnMeter ** 2)

    return bmi

# BMR menggunakan rumus Mifflin-St Jeor
def bmrCount(berat_badan, tinggi_badan, usia):
    bmr = 10 * berat_badan + 6.25 * tinggi_badan - 5 * usia - 161
    return bmr

# menghitung TDEE berdasarkan BMR dan tingkat aktivitas fisik (PAL)
def hitungTdee(bmr, pal):
    tdee = bmr * pal
    return tdee

# hitung by AKG kemenkes untuk Ibu hamil
def kaloriHarian(berat_badan, tinggi_badan, usia, pal, trimester, mode="AKG"):
    bmi = bmiCount(berat_badan, tinggi_badan)
    bmr = bmrCount(berat_badan, tinggi_badan, usia)
    tdee = hitungTdee(bmr, pal)

    if mode == "AKG" :
        if trimester == 1 :
            kalori_harian = tdee + 180
        elif trimester == 2 or trimester ==3 :
            kalori_harian = tdee + 300

    else :
        if trimester == 2 :
            kalori_harian = tdee + 340
        if trimester == 3 :
            kalori_harian = tdee + 450
        else :
            kalori_harian = tdee
    
    return bmi, tdee, kalori_harian

def pal_to_number(pal_enum):
    pal_values = {
        PAL.sedentary: 1.2,
        PAL.lightly_active: 1.375,
        PAL.moderately_active: 1.55,
        PAL.very_active: 1.725,
        PAL.super_active: 1.9
    }
    return pal_values.get(pal_enum, 1.2)

def update_gizi(user_id: str, berat_badan: float, tinggi_badan: float, usia: int, pal: float, trimester: int, db: Session):
    # Ambil data user berdasarkan nik (id)
    user = db.query(User).filter(User.nik == user_id).first()
    
    if not user:
        return {"message": "User not found"}
    
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
    
    # Hitung kalori harian
    bmr = 10 * berat_badan + 6.25 * tinggi_badan - 5 * usia - 161  # Rumus BMR Mifflin-St Jeor
    kalori_harian = kalori_harian(bmr, pal, trimester)

    # Perbarui atau buat data di tabel gizi
    gizi = db.query(Gizi).filter(Gizi.nik == user_id).first()
    
    if not gizi:
        # Jika belum ada data gizi, buat baru
        gizi = Gizi(nik=user_id, bmi=bmi, status_bmi=status_bmi, kalori_harian=kalori_harian)
        db.add(gizi)
    else:
        # Jika sudah ada, perbarui data gizi
        gizi.bmi = bmi
        gizi.status_bmi = status_bmi
        gizi.kalori_harian = kalori_harian

    db.commit()
    db.refresh(gizi)
    
    return {
        "message": f"Data updated successfully for user {user_id}",
        "bmi": bmi,
        "status_bmi": status_bmi,
        "kalori_harian": kalori_harian
    }