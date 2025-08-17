# test_model_load_only.py

from tensorflow.keras.models import load_model

try:
    model = load_model("efficientnet_v2s_dev_reduce.h5")

    print("✅ 模型加载成功")
except Exception as e:
    print("❌ 模型加载失败:", e)
