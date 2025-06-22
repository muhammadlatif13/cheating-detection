import os
import pandas as pd

FRAUD_IMAGES_DIR = 'data/fraud_data/fraud_captured/'
LOG_FILE_PATH = 'data/fraud_data/fraud_detection.csv'

def load_fraud_images():
    if not os.path.exists(FRAUD_IMAGES_DIR):
        os.makedirs(FRAUD_IMAGES_DIR)
    return [
        os.path.join(FRAUD_IMAGES_DIR, img_name)
        for img_name in sorted(os.listdir(FRAUD_IMAGES_DIR))
        if img_name.endswith('.png')
    ]

def load_log_data():
    if not os.path.exists(LOG_FILE_PATH):
        return pd.DataFrame(columns=['Timestamp', 'Level', 'Message'])

    with open(LOG_FILE_PATH, 'r') as f:
        logs = f.readlines()

    log_data = []
    for log in logs:
        try:
            timestamp, level, message = log.split(' - ', 2)
            log_data.append({'Timestamp': timestamp.strip(), 'Level': level.strip(), 'Message': message.strip()})
        except ValueError:
            log_data.append({'Timestamp': 'Invalid Format', 'Level': 'Error', 'Message': log.strip()})

    return pd.DataFrame(log_data)
