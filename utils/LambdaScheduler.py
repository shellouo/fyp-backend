import tensorflow as tf
from tensorflow.keras.layers import Layer

class LambdaScheduler(tf.keras.callbacks.Callback):
    def __init__(self, grl_layers, lambda_max, total_epochs):
        super().__init__()
        self.grl_layers = grl_layers
        self.lambda_max = lambda_max
        self.total_epochs = total_epochs

    def on_epoch_begin(self, epoch, logs=None):
        current_lambda = self.lambda_max * epoch / (self.total_epochs - 1)
        for grl in self.grl_layers:
            grl.set_lambda(current_lambda)
        print(f"Set GRL λ to {current_lambda:.4f}")