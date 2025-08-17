# app/model.py
import os
import numpy as np
import tensorflow as tf
from typing import Dict
from app.preprocess import preprocess_image  # 约定签名：preprocess_image(bytes, size) -> np.ndarray

# 训练/导出时用的输入尺寸，务必与 notebook 保持一致
INPUT_SIZE = (300, 300)

# 全局缓存，避免重复加载（性能关键）
_model = None

def load_age_model():
    """只在首次调用时从磁盘加载模型，后续复用内存中的实例。"""
    global _model
    if _model is None:
        # 统一到 weights/ 下，避免相对路径在不同工作目录下失效
        model_path = os.path.join(os.getcwd(), "weights", "efficientnet_v2s_dev.h5")
        _model = tf.keras.models.load_model(model_path, compile=False)
    return _model


def infer_from_array(img_bchw: np.ndarray) -> Dict:
    """
    输入：预处理后的 (1, H, W, C) float32 ∈ [0,1]
    输出：可直接 JSON 序列化的结果字典
    说明：你的模型输出顺序为 (age_pred, gender_pred, race_pred)
    """
    mdl = load_age_model()
    age_pred, gender_pred, race_pred = mdl.predict(img_bchw, verbose=0)

    # 年龄（回归）
    age = int(age_pred[0][0])

    # 性别（二分类 Sigmoid，阈值 0.5）
    raw_gender = float(gender_pred[0][0])
    gender = "Male" if raw_gender < 0.5 else "Female"
    gender_conf = round(1 - raw_gender if gender == "Male" else raw_gender, 4)

    # 种族（Softmax 多分类）
    race_labels = ["White", "Black", "Asian", "Indian", "Others"]
    race_idx = int(np.argmax(race_pred[0]))
    race = race_labels[race_idx]
    race_conf = round(float(np.max(race_pred[0])), 4)

    return {
        "age": age,
        "gender": gender,
        "gender_confidence": gender_conf,
        "race": race,
        "race_confidence": race_conf,
    }


def predict_image_path(image_path: str) -> Dict:
    """
    给定文件路径做一次完整预测（便于本地/Notebook测试）。
    生产环境路由更推荐走 bytes 预处理（参见 /predict）。
    """
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    arr = preprocess_image(img_bytes, size=INPUT_SIZE)  # -> (1,H,W,C)
    return infer_from_array(arr)
