# quick_test.py
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# ===== 改成你的模型目录和测试图片路径 =====
MODEL_DIR  = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0"
TEST_IMAGE = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\test.jpg"

# 固定224，因为SavedModel签名要求 (None,224,224,3)
TARGET_SIZE = (224, 224)

def basic_preprocess(path):
    img = Image.open(path).convert("RGB").resize(TARGET_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, 0)  # (1,H,W,3)

def main():
    print("[Load] tf.saved_model.load ...")
    loaded = tf.saved_model.load(MODEL_DIR)
    fn = loaded.signatures["serving_default"]
    _, kw = fn.structured_input_signature
    input_key = list(kw.keys())[0]
    print("[Sig] input key:", input_key)

    x = basic_preprocess(TEST_IMAGE)
    out = fn(**{input_key: tf.constant(x)})

    print("[Pred] output keys:", list(out.keys()))
    for k, v in out.items():
        arr = v.numpy()
        print(f"{k}: shape={arr.shape}, sample={arr[0]}")

if __name__ == "__main__":
    main()
