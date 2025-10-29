from datetime import date

def trisemesterCount(tanggal_kehamilan_pertama:date) -> int:
    today = date.today()

    selisihHari = (today - tanggal_kehamilan_pertama).days

    mingguKehamilan = selisihHari // 7

    if mingguKehamilan <= 12 :
        return "trisemester1"
    elif 13 <= mingguKehamilan <= 26 :
        return "trisemester2"
    elif 27 <= mingguKehamilan <= 40:
        return "trisemester3"
    else :
        return "postsemester"