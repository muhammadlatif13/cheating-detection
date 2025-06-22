import bcrypt
from db.connectDB import getConnectionDB

def create_user(username: str, password: str):
    conn = getConnectionDB()
    cursor = conn.cursor()

    # Hash password sebelum disimpan
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return {"status": "success", "message": "User created successfully"}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()
