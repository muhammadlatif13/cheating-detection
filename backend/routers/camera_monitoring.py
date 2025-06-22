# camera_monitoring.py

import cv2
import time
import base64
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from psycopg2.extras import RealDictCursor
from datetime import datetime

from db.connectDB import getConnectionDB
from db.fraudLogs import saveLogToDB
from utils.get_cameras import get_connected_cameras
from utils.detection.eye_gaze import detect_eye_gaze
from utils.detection.head_pose import detect_head_pose
from utils.detection.lip_movement import detect_lip_movement 
from utils.detection.cheating_model import CheatingDetector

router = APIRouter()
cheating_detector = CheatingDetector("models/cheating_detection_final4.keras")

fraud_count = 0
fraud_accumulated_time = 0
streaming_flag = False
notifications = [] 

def capture_and_process_frame(frame, fraud_type, fraud_count, fraud_accumulated_time, description=""):
    try:
        _, image_bytes = cv2.imencode('.png', frame)
        image_data = image_bytes.tobytes()
        
        classification_result, confidence_percentage = cheating_detector.predict(frame)
        
        if fraud_type in ["Peringatan kepada peserta ujian!!!", "CURANG"]:
            notification = {
                "id": len(notifications) + 1,
                "fraud_type": fraud_type,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "confidence_percentage": confidence_percentage,
                "read": False
            }
            notifications.append(notification)
        
        saveLogToDB(
            fraud_type=fraud_type,
            fraud_count=fraud_count,
            fraud_accumulated_time=fraud_accumulated_time,
            image_data=image_data,
            description=description,
            classification_result=classification_result,
            confidence_percentage=confidence_percentage
        )
        
        return True
    except Exception as e:
        print(f"Error in capture_and_process_frame: {e}")
        return False
    
def check_fraud_conditions(head_pose, eye_gaze, lip_movement, start_time, threshold_timing, fraud_tolerance, frame, description=""):
    global fraud_count, fraud_accumulated_time
    current_time = time.time()
    time_elapsed = current_time - start_time

    if head_pose == "Tidak Terdeteksi" and eye_gaze == "Tidak Terdeteksi" and lip_movement == "Tidak Terdeteksi":        
        if head_pose == "Tengah":
            if eye_gaze == "Tidak Terdeteksi" and lip_movement in ["Tutup", "Buka"]:
                return "Mata tidak terdeteksi kamera", current_time
            elif eye_gaze == "Tidak Terdeteksi" and lip_movement == "Tidak Terdeteksi":
                return "Mata dan mulut tidak terdeteksi kamera", current_time
        return "Peserta tidak terdeteksi", current_time

    if head_pose == "Tengah" and eye_gaze == "Tengah" and lip_movement in ["Tutup", "Buka"]:
        return "Normal", current_time

    if head_pose not in ["Tengah", "Tidak Terdeteksi"] or eye_gaze not in ["Tengah", "Berkedip", "Tidak Terdeteksi"]:
        fraud_accumulated_time += time_elapsed

        if head_pose not in ["Tengah", "Tidak Terdeteksi"]:
            description += f"Kepala mengarah ke {head_pose.lower()}"
        if eye_gaze not in ["Tengah", "Berkedip", "Tidak Terdeteksi"]:
            if description:
                description += " dan "
            description += f"peserta melirik ke {eye_gaze.lower()}"

        if fraud_accumulated_time >= threshold_timing:
            fraud_count += 1
            fraud_accumulated_time = 0 
            fraud_type = "Peringatan kepada peserta ujian!!!"
            
            try:
                capture_and_process_frame(
                    frame=frame,
                    fraud_type=fraud_type,
                    fraud_count=fraud_count,
                    fraud_accumulated_time=fraud_accumulated_time,
                    description=description
                )
            except Exception as e:
                print(f"Failed to save fraud log: {e}")
                return "Error saving log", current_time
            
            if fraud_count >= fraud_tolerance:
                fraud_type = "CURANG"
                try:
                    capture_and_process_frame(
                        frame=frame,
                        fraud_type=fraud_type,
                        fraud_count=fraud_count,
                        fraud_accumulated_time=fraud_accumulated_time,
                        description=description
                    )
                except Exception as e:
                    print(f"Failed to save fraud log: {e}")
                    return "Error saving log", current_time

        return description or "Posisi peserta tidak normal", current_time

    return "Normal", current_time

def capture_fraud_image(frame, fraud_count):
    try:
        _, image_bytes = cv2.imencode('.png', frame)
        image_data = image_bytes.tobytes()  
        saveLogToDB(image_data, fraud_count)
    except Exception as e:
        print(f"Error capturing fraud image: {e}")

def generate_frame(threshold_timing: int, fraud_tolerance: int, camera_id: int):
    global fraud_count, fraud_accumulated_time, streaming_flag

    cap = None
    current_camera_id = camera_id
    start_time = time.time()

    while streaming_flag:
        if cap is None or current_camera_id != camera_id:
            if cap:
                cap.release()
                cap = None  

            cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            if not cap.isOpened():
                raise RuntimeError(f"Failed to open camera with id {camera_id}")
            current_camera_id = camera_id
            
        ret, frame = cap.read()
        if not ret:
            break

        head_pose = detect_head_pose(frame)
        eye_gaze = detect_eye_gaze(frame)
        lip_movement = detect_lip_movement(frame)

        fraud_result, start_time = check_fraud_conditions(
            head_pose, eye_gaze, lip_movement, start_time, threshold_timing, fraud_tolerance, frame, description=""
        )

        if fraud_count >= fraud_tolerance:
            fraud_result = "CURANG"
            fraud_count = 0

        # Tampilkan informasi di frame
        cv2.putText(frame, f"Head Pose: {head_pose}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Eye Gaze: {eye_gaze}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Lip Movement: {lip_movement}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Fraud Status: {fraud_result}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Fraud Count: {fraud_count}", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Fraud Time Accumulated: {fraud_accumulated_time:.2f}s", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    if cap and cap.isOpened():
        cap.release()

@router.get("/api/get_cameras")
def get_cameras():
    cameras = get_connected_cameras()
    return cameras

@router.get("/video_feed")
def video_feed(threshold_timing: int = Query(10, ge=1, le=60), fraud_tolerance: int = Query(3, ge=1, le=20), camera_id: int = Query(0)):
    global streaming_flag
    streaming_flag = True  
    return StreamingResponse(generate_frame(threshold_timing, fraud_tolerance, camera_id), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/api/fraud_logs")
def get_fraud_logs():
    conn = getConnectionDB()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM fraud_logs ORDER BY id ASC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()

    for log in logs:
        if 'image_data' in log and log['image_data']:
            if isinstance(log['image_data'], str):
                log['image_data'] = log['image_data'].encode('utf-8')
            log['image_data'] = base64.b64encode(log['image_data']).decode('utf-8')

    return logs

@router.get("/api/notifications")
def get_notifications():
    return {"notifications": notifications}

@router.post("/api/notifications/{notification_id}/mark-read")
def mark_notification_read(notification_id: int):
    for notification in notifications:
        if notification["id"] == notification_id:
            notification["read"] = True
            return {"message": "Notification marked as read"}
    return {"error": "Notification not found"}, 404