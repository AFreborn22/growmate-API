from datetime import date

def ageCount(tanggal_lahir:date) -> int:
    today = date.today()
    age = today.year - tanggal_lahir.year

    if today.month < tanggal_lahir.month or (today.month == tanggal_lahir.month 
                                             and today.day < tanggal_lahir.day) :
        age-=1
    return age

