# quick_prep_infer.py
import tensorflow as tf
from pathlib import Path
from app.preprocess import preprocess_image_from_bytes_224_for_model

MODEL_DIR  = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0"
TEST_IMAGE = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\test.jpg"

def main():
    # 1. 加载模型
    loaded = tf.saved_model.load(MODEL_DIR)
    fn = loaded.signatures["serving_default"]

    # 2. 找到输入 key
    in_key = list(fn.structured_input_signature[1].keys())[0]
    print("[Sig] 模型输入 key:", in_key)

    # 3. 读取并预处理图片
    img_bytes = Path(TEST_IMAGE).read_bytes()
    x, dbg = preprocess_image_from_bytes_224_for_model(img_bytes, return_debug=True)

    if x is None:
        print("❌ 没检测到人脸:", dbg)
        return

    print("[Prep] 预处理后形状:", x.shape, "dtype:", x.dtype)

    # 4. 模型预测
    outputs = fn(**{in_key: tf.constant(x)})

    # 5. 打印输出
    for k, v in outputs.items():
        arr = v.numpy()
        print(f"[Pred] {k}: shape={arr.shape}, sample={arr[0] if arr.ndim==2 else arr}")

    # 6. 调试信息
    print("[Debug]", dbg)

if __name__ == "__main__":
    main()
