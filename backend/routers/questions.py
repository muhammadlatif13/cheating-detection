from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from db.connectDB import getConnectionDB
import json

router = APIRouter()

class Question(BaseModel):
    exam_id: int
    question: dict
    answer: str

class QuestionList(BaseModel):
    questions: List[Question]

@router.get("/add_questions/{exam_id}")
def get_questions(exam_id: int):
    conn = getConnectionDB()
    cursor = conn.cursor()
    cursor.execute("SELECT id, exam_id, question, answer FROM exam_questions WHERE exam_id = %s", (exam_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [{"id": q[0], "exam_id": q[1], "question": q[2], "answer": q[3]} for q in questions]

@router.post("/add_questions")
def add_questions(question_list: QuestionList):
    try:
        conn = getConnectionDB()
        cursor = conn.cursor()

        for question_data in question_list.questions:
            exam_id = question_data.exam_id
            question = json.dumps(question_data.question)
            answer = question_data.answer
            cursor.execute(
                "INSERT INTO exam_questions (exam_id, question, answer, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())",
                (exam_id, question, answer),
            )

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"{len(question_list.questions)} Soal berhasil ditambahkan"}

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))