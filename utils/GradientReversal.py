import tensorflow as tf
from tensorflow.keras.layers import Layer

class GradientReversal(Layer):
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
