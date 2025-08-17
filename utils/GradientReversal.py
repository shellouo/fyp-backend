import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import backend as K

class GradientReversal(Layer):
    def __init__(self, max_lambda=1.0, **kwargs):
        super(GradientReversal, self).__init__(**kwargs)
        self._lambda = tf.Variable(0.0, trainable=False, dtype=tf.float32)
        self.max_lambda = max_lambda

    def call(self, x):
        @tf.custom_gradient
        def reverse_gradient(x):
            def grad(dy):
                # return -self.max_lambda * dy  # 关键点：梯度反转
                return -self._lambda * dy
            return x, grad
        return reverse_gradient(x)

    def set_lambda(self, new_lambda):
        new_lambda = min(float(new_lambda), self.max_lambda)
        self._lambda.assign(new_lambda)

    def get_config(self):
        config = super().get_config()
        # config.update({"max_lambda": self.max_lambda})
        config.update({
            "max_lambda": self.max_lambda,
        })
        return config

