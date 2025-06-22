from utils.detection.gaze_tracking import GazeTracking

gaze = GazeTracking()

def detect_eye_gaze(frame):
    gaze.refresh(frame)

    if gaze.is_blinking():
        return "Berkedip"
    elif gaze.is_right():
        return "Kanan"
    elif gaze.is_left():
        return "Kiri"
    elif gaze.is_center():
        return "Tengah"
    return "Tidak Terdeteksi"