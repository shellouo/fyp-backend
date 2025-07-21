import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from mtcnn import MTCNN

detector = MTCNN()

def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)

    faces = detector.detect_faces(image_np)
    if not faces:
        raise ValueError("No face detected.")

    x, y, w, h = faces[0]['box']
    x, y = max(0, x), max(0, y)
    face = image_np[y:y+h, x:x+w]

    face_resized = cv2.resize(face, (224, 224))
    face_normalized = face_resized / 255.0
    return np.expand_dims(face_normalized, axis=0)
