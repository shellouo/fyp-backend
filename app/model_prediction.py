import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from app.preprocess import preprocess_image_from_bytes_224_for_model

#Implementation of GradientReversal used during training
class GradientReversal(tf.keras.layers.Layer):
    def __init__(self, max_lambda=1.0, **kwargs):
        super().__init__(**kwargs)
        self.max_lambda = max_lambda
        self.lambda_val = self.add_weight(
            name="lambda_val",
            shape=(),
            initializer="zeros",
            trainable=False
        )

    def call(self, x):
        lambda_tensor = self.lambda_val

        @tf.custom_gradient
        def reverse_gradient(x):
            def grad(dy):
                return -lambda_tensor * dy
            return x, grad

        return reverse_gradient(x)

    def set_lambda(self, new_lambda):
        new_lambda = min(float(new_lambda), self.max_lambda)
        self.lambda_val.assign(new_lambda)

    def get_config(self):
        config = super().get_config()
        config.update({
            "max_lambda": self.max_lambda,
        })
        return config

# Model path
MODEL_PATH = r"C:\Users\shell\PycharmProjects\PythonProject\fyp_backend\final model\model_efficientnetv2s_dev0.h5"
RACE_LABELS = ["RaceA", "RaceB", "RaceC", "RaceD", "RaceE"]
# Load model (with custom layer registration)
model = load_model(MODEL_PATH, custom_objects={"GradientReversal": GradientReversal})

# Decode output
def _decode_outputs(outputs):
    o0, o1, o2 = outputs

    age = float(o0[0][0])
    age = max(0.0, min(120.0, age))

    p_male = float(o1[0][0])
    gender = "Male" if p_male >= 0.5 else "Female"
    gender_conf = p_male if gender == "Male" else (1 - p_male)

    vec = o2[0]
    idx = int(np.argmax(vec))
    race = RACE_LABELS[idx]
    race_conf = float(vec[idx])

    return age, gender, gender_conf, race, race_conf

# Inference function
def predict_and_display(image_path: str):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    x = preprocess_image_from_bytes_224_for_model(
        img_bytes,
        use_effnetv2_preprocess=False,
        return_debug=False
    )
    if x is None:
        raise ValueError("No face detected or preprocess failed")

    outputs = model.predict(x)

    print("Raw outputs:")
    print("output_0:", outputs[0])
    print("output_1:", outputs[1])
    print("output_2:", outputs[2])

    return _decode_outputs(outputs)

