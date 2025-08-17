# app/preprocess.py 中新增（不覆盖你已有函数）
import io
import numpy as np
import cv2
from PIL import Image, ImageOps
from mtcnn import MTCNN

# —— 全局缓存 MTCNN，避免反复初始化 —— #
_DETECTOR = None
def _get_detector():
    global _DETECTOR
    if _DETECTOR is None:
        _DETECTOR = MTCNN()
    return _DETECTOR

def _read_rgb_fix_exif(image_bytes: bytes) -> np.ndarray:
    """bytes → RGB ndarray (H,W,3), 处理EXIF旋转"""
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.exif_transpose(img).convert("RGB")
    return np.array(img)

def _denoise_rgb(rgb: np.ndarray, strength: int = 5) -> np.ndarray:
    """彩色去噪（轻度），避免过强抹掉细节"""
    # OpenCV 需要 8-bit BGR
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    den = cv2.fastNlMeansDenoisingColored(bgr, None, h=strength, hColor=strength, templateWindowSize=7, searchWindowSize=21)
    return cv2.cvtColor(den, cv2.COLOR_BGR2RGB)

def _select_face(faces):
    """选面积×置信度最大的脸"""
    def score(f):
        x, y, w, h = f["box"]
        area = max(1, w*h)
        conf = float(f.get("confidence", 1.0))
        return area * conf
    return max(faces, key=score)

def _rotate_by_eyes(rgb: np.ndarray, left_eye, right_eye) -> np.ndarray:
    """根据双眼连线做仿射旋转，让眼睛水平"""
    (lx, ly), (rx, ry) = np.array(left_eye), np.array(right_eye)
    angle = np.degrees(np.arctan2(ry - ly, rx - lx))
    h, w = rgb.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(rgb, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def _square_crop_with_margin(rgb: np.ndarray, box, margin_ratio=0.3) -> np.ndarray:
    """以人脸框为中心加边距，裁正方形"""
    x, y, w, h = box
    cx, cy = x + w / 2, y + h / 2
    side = int(max(w, h) * (1.0 + margin_ratio))
    x1, y1 = int(cx - side / 2), int(cy - side / 2)
    x2, y2 = x1 + side, y1 + side
    H, W = rgb.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(W, x2), min(H, y2)
    crop = rgb[y1:y2, x1:x2]
    return crop

def _white_background_mask(crop: np.ndarray, softness: float = 0.08) -> np.ndarray:
    """
    把正方形裁剪图的背景变白：用椭圆区域保留中心人脸，外部渐变到白色。
    softness: 边缘软化比例，0.0~0.5
    """
    h, w = crop.shape[:2]
    mask = np.zeros((h, w), np.float32)
    # 椭圆覆盖 90% 边长
    ax, ay = int(w * 0.45), int(h * 0.45)
    center = (w // 2, h // 2)
    cv2.ellipse(mask, center, (ax, ay), 0, 0, 360, 1.0, -1)
    # 边缘软化
    k = max(3, int(min(h, w) * softness) | 1)
    mask = cv2.GaussianBlur(mask, (k, k), 0)
    mask = mask[..., None]  # (H,W,1)
    white = np.full_like(crop, 255, dtype=np.uint8)
    blended = (crop.astype(np.float32) * mask + white.astype(np.float32) * (1 - mask)).astype(np.uint8)
    return blended

def preprocess_image_from_bytes_224_for_model(
    image_bytes: bytes,
    use_effnetv2_preprocess: bool = False,   # 你当前 quick_test 用的是 /255.0，所以默认 False
    margin_ratio: float = 0.3,
    align_by_eyes: bool = True,
    whiten_background: bool = True,
    return_debug: bool = False,
):
    """
    满足老师与模型的双重要求：
    - 降噪 → 人脸检测（多人脸择优）→ (可选)对齐 → 正方形裁剪 + 白背景 → resize 224 → 归一化
    - 输出：(1,224,224,3), float32, 像素在 [0,1]（或EffNetV2预处理后范围）
    - 未检测到人脸返回 None（符合“无脸时提示/处理”的要求）
    """
    debug = {}

    # 1) 解码 + EXIF 矫正 + RGB
    try:
        rgb = _read_rgb_fix_exif(image_bytes)
    except Exception:
        return None if not return_debug else (None, {"error": "decode_fail"})

    # 2) 轻度去噪
    rgb = _denoise_rgb(rgb, strength=5)

    # 3) 人脸检测（可先按长边≤1280等比例缩小以提速，需注意回映射；此处直接原图）
    det = _get_detector()
    faces = det.detect_faces(rgb)
    if not faces:
        return (None if not return_debug else (None, {"error": "no_face"}))

    best = _select_face(faces)
    box = best["box"]  # (x,y,w,h)
    keypoints = best.get("keypoints", {})
    debug["mtcnn_box"] = box
    debug["mtcnn_score"] = float(best.get("confidence", 1.0))

    # 4) 可选：按双眼对齐后重新取一次人脸框
    if align_by_eyes and "left_eye" in keypoints and "right_eye" in keypoints:
        rgb = _rotate_by_eyes(rgb, keypoints["left_eye"], keypoints["right_eye"])
        faces2 = det.detect_faces(rgb)
        if faces2:
            best2 = _select_face(faces2)
            box = best2["box"]
            debug["mtcnn_box_after_align"] = box
            debug["mtcnn_score_after_align"] = float(best2.get("confidence", 1.0))

    # 5) 正方形裁剪（含 margin）
    crop = _square_crop_with_margin(rgb, box, margin_ratio=margin_ratio)
    if crop.size == 0:
        return (None if not return_debug else (None, {"error": "empty_crop"}))

    # 6) 背景白化（椭圆保脸，边缘柔化）
    if whiten_background:
        crop = _white_background_mask(crop, softness=0.08)

    # 7) 缩放 → 224×224（下采样用 INTER_AREA 更稳）
    crop224 = cv2.resize(crop, (224, 224), interpolation=cv2.INTER_AREA)

    # 8) 归一化 → 与 quick_test 保持一致（/255.0）
    x = crop224.astype(np.float32)
    if use_effnetv2_preprocess:
        # 如你后续确认训练用的是EffNetV2预处理，可切 True
        from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
        x = preprocess_input(x)
    else:
        x = x / 255.0

    x = np.expand_dims(x, 0)  # (1,224,224,3)

    return (x if not return_debug else (x, debug))
