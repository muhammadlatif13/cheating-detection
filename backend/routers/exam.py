from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.connectDB import getConnectionDB

router = APIRouter()

class Exam(BaseModel):
    nama_ujian: str
    durasi: int
    jumlah_soal: int

@router.get("/exam")
def get_exams():
    conn = getConnectionDB()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nama_ujian, durasi, jumlah_soal FROM exams")
    exams = cursor.fetchall()

    print("Hasil query dari database:", exams)

    result = []
    for e in exams:
        result.append({
            "id": e[0],
            "nama_ujian": e[1],
            "durasi": e[2],
            "jumlah_soal": e[3]
        })

    print("Data yang dikirim ke frontend:", result)
    
    cursor.close()
    conn.close()
    return result

@router.post("/exam")
def create_exam(exam: Exam):
    conn = getConnectionDB()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO exams (nama_ujian, durasi, jumlah_soal) VALUES (%s, %s, %s) RETURNING id",
            (exam.nama_ujian, exam.durasi, exam.jumlah_soal)
        )
        exam_id = cursor.fetchone()[0]
        conn.commit()
        return {"message": "Exam added successfully", "id": exam_id}
    except Exception as e:
        conn.rollback()
        print(f"SQL Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    
@router.get("/exam/{exam_id}")
def get_exam(exam_id: int):
    conn = getConnectionDB()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_ujian FROM exams WHERE id = %s", (exam_id,))
    exams = cursor.fetchone()
    cursor.close()
    conn.close()
    if not exams:
        raise HTTPException(status_code=404, detail="Ujian tidak ditemukan")
    return {"id": exams[0], "nama_ujian": exams[1]}
        
@router.put("/exam/{exam_id}")
def update_exam(exam_id: int, exam: Exam):
    conn = getConnectionDB()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE exams 
            SET nama_ujian = %s, durasi = %s, jumlah_soal = %s
            WHERE id = %s
            """,
            (exam.nama_ujian, exam.durasi, exam.jumlah_soal, exam_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ujian tidak ditemukan")

        return {"message": "Data ujian berhasil diperbarui"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()