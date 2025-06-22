import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
    )

def detect_head_pose(frame):
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_h, img_w, _ = frame.shape
    text = ""

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            face_2d, face_3d = [], []
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            cam_matrix = np.array([[img_w, 0, img_w / 2],
                                    [0, img_w, img_h / 2],
                                    [0, 0, 1]], dtype=np.float64)
            dist_matrix = np.zeros((4, 1), dtype=np.float64)
            success, rot_vec, _ = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            if success:
                rmat, _ = cv2.Rodrigues(rot_vec)
                angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
                x_angle = angles[0] * 360
                y_angle = angles[1] * 360

                if y_angle < -15:
                    text = "Kanan"
                elif y_angle > 15:
                    text = "Kiri"
                elif x_angle < -7.5:
                    text = "Bawah"
                elif x_angle > 12.5:
                    text = "Atas"
                else:
                    if abs(y_angle) < 15:
                        text = "Tengah"
    else:
        text = "Tidak Terdeteksi"
    return text