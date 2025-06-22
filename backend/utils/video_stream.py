import cv2
import time
from db.fraudLogs import saveLogToDB
from utils.detection.eye_gaze import detect_eye_gaze
from utils.detection.head_pose import detect_head_pose
from utils.detection.lip_movement import detect_lip_movement
from utils.detection.people_tracking import detect_people

# Global variables
fraud_count = 0
fraud_accumulated_time = 0
streaming_flag = False

def set_streaming_flag(flag):
    global streaming_flag
    streaming_flag = flag

def check_fraud_conditions(head_pose, eye_gaze, lip_movement, people_count, start_time, threshold_timing, fraud_tolerance, image_data, description=""):
    global fraud_count, fraud_accumulated_time
    current_time = time.time()
    time_elapsed = current_time - start_time

    if people_count > 1:
        fraud_accumulated_time += time_elapsed
        description = f"Terdeteksi {people_count} orang dalam frame" 
        
        if fraud_accumulated_time >= threshold_timing:
            fraud_count += 1
            fraud_accumulated_time = 0
            # Sesuaikan parameter agar sesuai dengan definisi fungsi di db/fraudLogs.py
            try:
                fraud_type = "Peringatan kepada peserta ujian!!!"
                saveLogToDB(fraud_type=fraud_type, count=fraud_count, time=fraud_accumulated_time, image_data=image_data, description=description)
                
                if fraud_count >= fraud_tolerance:
                    fraud_type = "CURANG"
                    saveLogToDB(fraud_type=fraud_type, count=fraud_count, time=fraud_accumulated_time, image_data=image_data, description=description)
            except Exception as e:
                print(f"Error saving fraud log to DB: {e}")
                
        return description, current_time

    # Jika tidak ada orang yang terdeteksi
    if people_count == 0:
        return "Peserta tidak terdeteksi", current_time

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
            saveLogToDB(fraud_type, fraud_count, fraud_accumulated_time, image_data, description)  
            
            if fraud_count >= fraud_tolerance:
                fraud_type = "CURANG"
                saveLogToDB(fraud_type, fraud_count, fraud_accumulated_time, image_data, description)

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
                print(f"Releasing camera {current_camera_id}")
                cap.release()
                print(f"Camera {current_camera_id} released")
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
        people_count, frame_with_detection = detect_people(frame)
        
        _, image_bytes = cv2.imencode('.png', frame)
        image_data = image_bytes.tobytes()

        fraud_result, start_time = check_fraud_conditions(
            head_pose, eye_gaze, lip_movement, people_count, start_time, 
            threshold_timing, fraud_tolerance, image_data, description=""
        )

        if fraud_count >= fraud_tolerance:
            fraud_result = "CURANG"
            capture_fraud_image(frame, fraud_count)
            fraud_count = 0

        # Menggunakan frame dengan hasil deteksi orang
        frame = frame_with_detection
        
        cv2.putText(frame, f"Head Pose: {head_pose}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Eye Gaze: {eye_gaze}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Lip Movement: {lip_movement}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"People Tracking: {people_count}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Fraud Status: {fraud_result}", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Fraud Count: {fraud_count}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Fraud Time Accumulated: {fraud_accumulated_time:.2f}s", (20, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    if cap:
        cap.release()