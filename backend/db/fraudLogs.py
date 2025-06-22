from db.connectDB import getConnectionDB

def saveLogToDB(fraud_type, fraud_count, fraud_accumulated_time, image_data, description="", classification_result="", confidence_percentage=0.0):
    conn = getConnectionDB()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO fraud_logs 
            (fraud_type, fraud_count, fraud_accumulated_time, image_data, description, classification_result, confidence_percentage, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (fraud_type, fraud_count, fraud_accumulated_time, image_data, description, classification_result, confidence_percentage)
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving fraud log: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
