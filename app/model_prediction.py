# app/model_prediction.py
import os
from pathlib import Path
import numpy as np
import tensorflow as tf

# ✅ 修改这里：SavedModel 目录（包含 saved_model.pb 的那个文件夹）
MODEL_DIR = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0"

# ✅ 修改这里：5个类别名（顺序必须与训练softmax输出一致）
RACE_LABELS = ["RaceA", "RaceB", "RaceC", "RaceD", "RaceE"]

# 用你刚才写好的预处理（bytes -> (1,224,224,3) float32 in [0,1]）
from app.preprocess import preprocess_image_from_bytes_224_for_model

# ---- 缓存加载 SavedModel + 找到输入键 ----
_fn = None
_input_key = None
def _get_signature():
    global _fn, _input_key
    if _fn is not None:
        return _fn, _input_key

    assert os.path.isfile(os.path.join(MODEL_DIR, "saved_model.pb")), f"SavedModel 目录无效: {MODEL_DIR}"
    loaded = tf.saved_model.load(MODEL_DIR)
    fn = loaded.signatures.get("serving_default") or next(iter(loaded.signatures.values()))
    _, kw = fn.structured_input_signature
    if not kw:
        raise RuntimeError("SavedModel 没有可用的输入签名")
    input_key = list(kw.keys())[0]
    _fn, _input_key = fn, input_key
    return _fn, _input_key

def _decode_outputs(out_dict: dict):
    """
    out_dict keys 形如: 'output_0'(1,1) 年龄回归, 'output_1'(1,1) 性别sigmoid, 'output_2'(1,5) softmax
    返回: (age, gender, gender_conf, race, race_conf)
    """
    o0 = out_dict["output_0"].numpy()  # (1,1)
    o1 = out_dict["output_1"].numpy()  # (1,1)
    o2 = out_dict["output_2"].numpy()  # (1,5)

    # 年龄
    age_val = float(o0[0, 0])
    age = max(0.0, min(120.0, age_val))  # 简单裁剪
    # 性别（假设输出为“Male 概率”）
    p_male = float(o1[0, 0])
    gender = "Male" if p_male >= 0.5 else "Female"
    gender_conf = p_male if gender == "Male" else (1.0 - p_male)
    # 5 类 softmax
    vec = o2[0]
    idx = int(np.argmax(vec))
    race = RACE_LABELS[idx] if 0 <= idx < len(RACE_LABELS) else f"Class{idx}"
    race_conf = float(vec[idx])

    return (age, gender, gender_conf, race, race_conf)

def predict_and_display(image_path: str):
    """
    供 routes.py 调用。
    输入: 图片绝对/相对路径
    返回: (age, gender, gender_conf, race, race_conf)
    异常: 未检到人脸/模型错误会抛出异常，routes.py 会捕获并返回 HTTP 500
    """
    p = Path(image_path)
    if not p.is_file():
        raise FileNotFoundError(f"图片不存在: {p}")

    img_bytes = p.read_bytes()

    # 预处理：与 quick_test 一致 → (1,224,224,3) float32, 归一化到 [0,1]
    x = preprocess_image_from_bytes_224_for_model(
        img_bytes,
        use_effnetv2_preprocess=False,   # 你当前链路用的是 /255.0；若确认用EffNetV2预处理，这里改 True
        return_debug=False
    )
    if x is None:
        # 交给 routes.py 统一转成 422 或 500
        raise ValueError("No face detected or preprocess failed")

    # 推理
    fn, input_key = _get_signature()
    outputs = fn(**{input_key: tf.constant(x)})

    # 解析为 5元组
    return _decode_outputs(outputs)
