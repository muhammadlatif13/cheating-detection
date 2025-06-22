import cv2
import dlib
import numpy as np

predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

def calculate_mouth_aspect_ratio(landmarks):
    top_lip = [landmarks.part(i) for i in range(48, 58)]
    bottom_lip = [landmarks.part(i) for i in range(58, 68)]
    
    top_lip_height = np.linalg.norm(np.array([top_lip[3].x, top_lip[3].y]) - np.array([top_lip[0].x, top_lip[0].y]))
    bottom_lip_height = np.linalg.norm(np.array([bottom_lip[3].x, bottom_lip[3].y]) - np.array([bottom_lip[0].x, bottom_lip[0].y]))
    
    lip_width = np.linalg.norm(np.array([top_lip[0].x, top_lip[0].y]) - np.array([top_lip[6].x, top_lip[6].y]))
    
    return (top_lip_height + bottom_lip_height) / (2.0 * lip_width)

def detect_lip_movement(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    if len(faces) == 0:
        return "Tidak Terdeteksi"

    for face in faces:
        landmarks = predictor(gray, face)
        mouth_aspect_ratio = calculate_mouth_aspect_ratio(landmarks)
        threshold = 0.55
        
        if mouth_aspect_ratio > threshold:
            label = "Buka"
        else:
            label = "Tutup"
    return label