# app/preprocess.py

import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from mtcnn import MTCNN

# 初始化人脸检测器（只加载一次）
detector = MTCNN()

def preprocess_image(image_bytes):
    """
    输入：原始图像的二进制数据（如 UploadFile.read()）
    输出：形状为 (1, 224, 224, 3) 的 numpy 数组，或 None（未检测到人脸）
    """

    try:
        # 1. 解码图像（转为 RGB）
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)

        # 2. 检测所有人脸
        faces = detector.detect_faces(image_np)
        if not faces:
            return None

        # 3. 选最大面积的人脸
        face = max(faces, key=lambda x: x['box'][2] * x['box'][3])
        keypoints = face['keypoints']
        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']

        # 4. 回正处理：根据眼睛角度矫正图像
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dy, dx))
        eye_center = ((left_eye[0] + right_eye[0]) // 2,
                      (left_eye[1] + right_eye[1]) // 2)
        rotation_matrix = cv2.getRotationMatrix2D(eye_center, angle, scale=1.0)
        rotated = cv2.warpAffine(image_np, rotation_matrix, (image_np.shape[1], image_np.shape[0]))

        # 5. 旋转后再次检测最大人脸
        faces_rotated = detector.detect_faces(rotated)
        if not faces_rotated:
            return None
        face_rot = max(faces_rotated, key=lambda x: x['box'][2] * x['box'][3])
        x, y, w, h = face_rot['box']
        x, y = max(0, x), max(0, y)

        # 6. 裁剪 + resize 成 224x224
        face_crop = rotated[y:y+h, x:x+w]
        face_resized = cv2.resize(face_crop, (300, 300))

        # 7. 归一化 + 添加 batch 维度
        face_normalized = face_resized / 255.0
        return np.expand_dims(face_normalized, axis=0)

    except Exception:
        return None
