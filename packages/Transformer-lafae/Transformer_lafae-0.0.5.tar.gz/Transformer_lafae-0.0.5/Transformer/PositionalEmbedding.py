import tensorflow as tf
from .aux_functions import positional_encoding

class PositionalEmbedding(tf.keras.layers.Layer):
    """
    A positional embedding layer combines the input features with a positional encoding.
    This layer adds positional information to the input features, aiding the model's understanding
    of sequential dependencies in regression tasks.

    Methods:
        call: Performs the forward pass of the layer.
    """
    def __init__(self, input_dim: int, d_model: int, max_sequence_length: int):
        """ Constructor of the PositionalEmbedding layer.

        Args:
            input_dim (int): The dimensionality of the input features.
            d_model (int): The dimensionality of the positional encoding vector.
            max_sequence_length (int): The maximum sequence length to consider for positional encoding.
        """
        super().__init__()
        self.d_model = d_model
        self.pos_encoding = positional_encoding(length=max_sequence_length, depth=d_model)

    def call(self, x: tf.Tensor) -> tf.Tensor:
        """ Performs the forward pass of the layer.
        
        Args:
            x (tf.Tensor): The input tensor of shape (batch_size, input_dim).

        Returns:
            tf.Tensor: The output tensor of shape (batch_size, input_dim + d_model),
                where the additional dimension corresponds to positional encoding.
        """
        length = tf.shape(x)[1]
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        pos_encoding = self.pos_encoding[tf.newaxis, :length, :]
        return tf.concat([x, pos_encoding], axis=-1)
