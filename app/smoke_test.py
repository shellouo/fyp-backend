# app/smoke_test.py
import os, sys
from pathlib import Path
import numpy as np
import tensorflow as tf

# ===== 把这个目录改成你的 SavedModel 目录（包含 saved_model.pb）=====
MODEL_DIR = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0"
TEST_IMAGE = r"test.jpg"  # 根目录放一张测试图

# ===== 与 SavedModel 签名保持一致：这里改成 224×224 =====
TARGET_SIZE = (224, 224)
USE_EFFNET_V2_PREPROCESS = True  # 若训练时用 /255.0，就设 False

# 让根目录进 sys.path，便于导入你现有的预处理
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# 用你写好的预处理函数（自动兼容两种函数名）
try:
    from app.preprocess import preprocess_image_from_bytes as prep_fn
except Exception:
    from app.preprocess import preprocess_image as prep_fn

# 可选：按需分配显存
try:
    for g in tf.config.list_physical_devices("GPU"):
        tf.config.experimental.set_memory_growth(g, True)
except Exception:
    pass

def main():
    assert os.path.isdir(MODEL_DIR), f"MODEL_DIR 不存在: {MODEL_DIR}"
    assert os.path.isfile(os.path.join(MODEL_DIR, "saved_model.pb")), "不是有效的 SavedModel 目录"

    print("[Load] tf.saved_model.load ...")
    loaded = tf.saved_model.load(MODEL_DIR)
    sig_names = list(loaded.signatures.keys())
    print("[Load] signatures:", sig_names)
    # 一般就是 'serving_default'
    fn = loaded.signatures.get("serving_default") or next(iter(loaded.signatures.values()))

    # 解析签名的输入键名和形状
    _, kw = fn.structured_input_signature
    assert len(kw) == 1, f"期望单输入，实际有 {len(kw)} 个: {list(kw.keys())}"
    input_key, spec = next(iter(kw.items()))
    print(f"[Sig] input key: {input_key}, required shape: {spec.shape}")

    # 读图 + 你的预处理（改成 224×224）
    with open(TEST_IMAGE, "rb") as f:
        img_bytes = f.read()
    try:
        x = prep_fn(img_bytes, target_size=TARGET_SIZE, use_effnet_v2_preprocess=USE_EFFNET_V2_PREPROCESS)
    except TypeError:
        x = prep_fn(img_bytes)

    if x is None:
        print("[Prep] 未检测到人脸/预处理失败"); return

    # 转 Tensor 并按签名“键名传参”
    x_tf = tf.constant(x, dtype=tf.float32)
    print("[Pred] calling SavedModel signature with kwargs...")
    out = fn(**{input_key: x_tf})  # dict -> Tensor(s)

    # 打印输出
    print("[Pred] output keys:", list(out.keys()))
    for k, v in out.items():
        arr = v.numpy()
        print(f"[Pred] {k}: shape={arr.shape}")
        if arr.ndim == 2 and arr.shape[1] > 1:
            print(f"       top_class={int(np.argmax(arr[0]))}, conf={float(np.max(arr[0]))}")
        else:
            print(f"       value={float(arr[0][0])}")

if __name__ == "__main__":
    main()
