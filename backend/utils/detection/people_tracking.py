import cv2
import numpy as np

def people_tracking():
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Error: Tidak bisa membuka webcam.")
        return
    
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")  
    
    tracks = {}  
    next_id = 0 
    max_disappeared = 30

    print("Pelacakan banyak orang dimulai. Tekan 'q' untuk keluar.")
    
    while True:
        ret, frame = cap.read() 
        if not ret:
            print("Error: Gagal menangkap frame.")
            break
            
        frame = cv2.resize(frame, (640, 480))  
        display = frame.copy() 
        results = model(frame, classes=0)  
        current_detections = []  
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w = x2 - x1 
                h = y2 - y1  
                conf = box.conf[0].item()  

                if conf > 0.75:
                    centroid_x = x1 + w // 2  
                    centroid_y = y1 + h // 2  
                    
                    current_detections.append({
                        "bbox": (x1, y1, w, h),
                        "centroid": (centroid_x, centroid_y),
                        "confidence": conf
                    })
        
        if tracks:
            for track_id in tracks:
                tracks[track_id]["disappeared"] += 1
            
            used_detections = set()
            
            for track_id, track in list(tracks.items()):
                if track["disappeared"] > max_disappeared:
                    del tracks[track_id]
                    continue
                    
                best_distance = float('inf')
                best_detection_idx = None
                
                for i, detection in enumerate(current_detections):
                    if i in used_detections:
                        continue
                    
                    track_centroid = track["centroid"]
                    detection_centroid = detection["centroid"]
                    
                    distance = np.sqrt(
                        (track_centroid[0] - detection_centroid[0]) ** 2 +
                        (track_centroid[1] - detection_centroid[1]) ** 2
                    )
                    
                    if distance < best_distance and distance < 100:  
                        best_distance = distance
                        best_detection_idx = i
                
                if best_detection_idx is not None:
                    detection = current_detections[best_detection_idx]
                    tracks[track_id]["bbox"] = detection["bbox"]
                    tracks[track_id]["centroid"] = detection["centroid"]
                    tracks[track_id]["confidence"] = detection["confidence"]
                    tracks[track_id]["disappeared"] = 0
                    used_detections.add(best_detection_idx)
            
            for i, detection in enumerate(current_detections):
                if i not in used_detections:
                    tracks[next_id] = {
                        "bbox": detection["bbox"],
                        "centroid": detection["centroid"],
                        "confidence": detection["confidence"],
                        "disappeared": 0,
                        "color": (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
                    }
                    next_id += 1
        else:
            for detection in current_detections:
                tracks[next_id] = {
                    "bbox": detection["bbox"],
                    "centroid": detection["centroid"],
                    "confidence": detection["confidence"],
                    "disappeared": 0,
                    "color": (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
                }
                next_id += 1
        
        active_tracks = 0
        for track_id, track in tracks.items():
            if track["disappeared"] <= 5:  
                active_tracks += 1
                x, y, w, h = track["bbox"]

                cv2.rectangle(display, (x, y), (x + w, y + h), track["color"], 2)
                
                confidence_text = f"{track['confidence']:.2f}" if "confidence" in track else ""
                cv2.putText(display, f"Person {track_id} {confidence_text}", 
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, track["color"], 2)
                cv2.circle(display, track["centroid"], 4, track["color"], -1)  
        
        cv2.putText(display, f"Tracking: {active_tracks} people", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Multi-Person Tracking', display)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Pelacakan orang dihentikan.")

if __name__ == "__main__":
    people_tracking()
