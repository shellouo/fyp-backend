import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from mtcnn import MTCNN

detector = MTCNN()

def preprocess_image(image_bytes):
    """
    输入：图像二进制数据（如 UploadFile.read()）
    输出：形状为 (1, 224, 224, 3) 的 numpy 数组，或 None（若检测失败）
    """

    try:
        # 1. 解码图片
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)

        # 2. 检测所有人脸
        faces = detector.detect_faces(image_np)
        if not faces:
            print("❌ 没有人脸")
            return None

        # 3. 选面积最大的人脸
        face = max(faces, key=lambda x: x['box'][2] * x['box'][3])
        box = face['box']
        keypoints = face['keypoints']
        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']

        # 4. 计算旋转角度（回正用）
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dy, dx))

        # 5. 图像绕眼睛中心点旋转
        eye_center = ((left_eye[0] + right_eye[0]) // 2,
                      (left_eye[1] + right_eye[1]) // 2)
        rotation_matrix = cv2.getRotationMatrix2D(eye_center, angle, scale=1.0)
        rotated = cv2.warpAffine(image_np, rotation_matrix, (image_np.shape[1], image_np.shape[0]))

        # 6. 旋转后再次检测人脸，找最大脸
        faces_rotated = detector.detect_faces(rotated)
        if not faces_rotated:
            print("❌ 回正后也没人脸")
            return None
        face_rot = max(faces_rotated, key=lambda x: x['box'][2] * x['box'][3])
        x, y, w, h = face_rot['box']
        x, y = max(0, x), max(0, y)

        # 7. 裁剪人脸区域并 resize
        face_crop = rotated[y:y+h, x:x+w]
        face_resized = cv2.resize(face_crop, (224, 224))

        # 8. 归一化 + batch维度
        face_normalized = face_resized / 255.0
        return np.expand_dims(face_normalized, axis=0)

    except Exception as e:
        print(f"⚠️ 图像预处理失败：{e}")
        return None
