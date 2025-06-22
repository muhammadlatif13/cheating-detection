import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

class CheatingDetector:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.class_names = ['Cheating', 'Normal']  
    
    def preprocess_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image_array = img_to_array(image)
        image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
        return np.expand_dims(image_array, axis=0)

    def predict(self, frame):
        try:
            processed_image = self.preprocess_image(frame)
            prediction = self.model.predict(processed_image, verbose=0)[0][0]  # sigmoid output (float)

            # Asumsi: prediction mendekati 1 berarti Cheating, mendekati 0 berarti Normal
            cheating_confidence = float(prediction)
            normal_confidence = 1.0 - cheating_confidence

            # Threshold 0.7 untuk Cheating
            if cheating_confidence >= 0.7:
                return self.class_names[1], cheating_confidence  # Cheating
            else:
                return self.class_names[0], normal_confidence  # Normal
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Error", 0.0

# # utils/detection/cheating_model.py
# import cv2
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model

# class CheatingDetector:
#     def __init__(self, model_path):
#         self.model = load_model(model_path)
#         self.class_names = ['Cheating', 'Normal'] 
    
#     def preprocess_image(self, image):
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image = cv2.resize(image, (224, 224))
#         image_array = img_to_array(image)
#         image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
#         return np.expand_dims(image_array, axis=0)

#     def predict(self, frame):
#         try:
#             processed_image = self.preprocess_image(frame)
#             prediction = self.model.predict(processed_image, verbose=0)[0][0]  # sigmoid output (float)

#             cheating_confidence = float(prediction)
#             normal_confidence = 1.0 - cheating_confidence

#             if cheating_confidence >= 0.7:
#                 return "Cheating", cheating_confidence
#             else:
#                 return "Normal", normal_confidence
#         except Exception as e:
#             print(f"Prediction error: {e}")
#             return "Error", 0.0
