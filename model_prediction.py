# model_predict/model_prediction.py
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

# 1) 尝试从真正的 utils 包导入 GradientReversal
try:
    # 确保你的 utils 是一个目录包：utils/__init__.py + utils/GradientReversal.py
    from utils.GradientReversal import GradientReversal  #
except Exception:

    class GradientReversal(tf.keras.layers.Layer):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
        def call(self, x):
            return x

# 3) 模型权重的**绝对路径**（相对本文件）
WEIGHTS = (Path(__file__).resolve().parent / ".." / "models" / "model_efficientnetv2s_dev0.h5").resolve()

def _load_model():
    with tf.keras.utils.custom_object_scope({'GradientReversal': GradientReversal}):
        model = tf.keras.models.load_model(str(WEIGHTS))
    return model

def predict_and_display(image_path: str):
    # 读取与预处理
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3, expand_animations=False)
    image = tf.image.resize(image, (224, 224))
    image = tf.cast(image, tf.float32)
    image = preprocess_input(image)
    image = tf.expand_dims(image, axis=0)

    # 加载模型并推理
    model = _load_model()
    age_pred, gender_pred, race_pred = model.predict(image)

    # 年龄
    age = int(round(float(age_pred[0][0])))

    # 性别与置信度（阈值 0.5；raw<0.5 => Male）
    raw_gender = float(gender_pred[0][0])
    gender = "Male" if raw_gender < 0.5 else "Female"
    gender_confidence = 1 - raw_gender if gender == "Male" else raw_gender

    # 种族与置信度
    race_labels = ["White", "Black", "Asian", "Indian", "Others"]
    race_idx = int(np.argmax(race_pred[0]))
    race = race_labels[race_idx]
    race_confidence = float(np.max(race_pred[0]))

    # 统一返回 5 元组
    return age, gender, gender_confidence, race, race_confidence
