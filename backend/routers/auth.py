from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

from db.connectDB import getConnectionDB

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

# Helper function to verify user credentials
def verify_user(username: str):
    conn = getConnectionDB()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

@router.post("/login")
def login(user: LoginRequest):
    user_data = verify_user(user.username)

    if not user_data:
        raise HTTPException(status_code=401, detail="Username atau password salah")

    if not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    return {
        "status": "success",
        "message": "Login berhasil",
        "token": "dummy-token",
        "role": user_data["role"]
    }

@router.post("/register")
async def register_user(user: UserCreate):
    conn = getConnectionDB()
    cursor = conn.cursor()

    hashed_password = pwd_context.hash(user.password)

    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Invalid role. Only 'admin' or 'user' allowed.")

    try:
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING id",
            (user.username, hashed_password, user.role)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        return {"message": "User registered successfully", "user_id": user_id, "role": user.role}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Database Error: Could not register user")
    finally:
        cursor.close()
        conn.close()

@router.post("/logout")
def logout():
    return {"status": "success", "message": "Logout berhasil"}