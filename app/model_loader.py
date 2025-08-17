# app/model_prediction.py
import tensorflow as tf
from .preprocess import preprocess_image_from_bytes

MODEL_DIR = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0"  # 改成绝对路径
TARGET_SIZE = (300, 300)  # 和训练一致
USE_EFFNET_V2_PREPROCESS = True  # 如果训练时用的是EffNetV2预处理

_model = None


def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_DIR, compile=False)
        print("[Model] Loaded SavedModel from:", MODEL_DIR)
        print("Input shape:", _model.input_shape)
        print("Output names:", _model.output_names)
    return _model


def predict_from_bytes(image_bytes: bytes):
    model = get_model()
    x = preprocess_image_from_bytes(
        image_bytes,
        target_size=TARGET_SIZE,
        use_effnet_v2_preprocess=USE_EFFNET_V2_PREPROCESS
    )
    if x is None:
        return None

    y = model.predict(x, verbose=0)

    # —— 注意：这里要根据你的输出头实际顺序来解包 —— #
    # 假设顺序是 [age, gender, race]
    if isinstance(y, (list, tuple)):
        age = float(y[0][0])
        gender_conf = float(y[1][0])
        race_conf = float(y[2][0])
    else:
        # 单头输出情况（可能是多分类，需再拆分）
        age = float(y[0][0]);
        gender_conf = 0.5;
        race_conf = 0.5

    gender = "Male" if gender_conf >= 0.5 else "Female"
    race = "Asian" if race_conf >= 0.5 else "Other"
    return age, gender, gender_conf, race, race_conf
