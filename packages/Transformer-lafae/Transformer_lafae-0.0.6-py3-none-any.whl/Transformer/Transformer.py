from .encoder import Encoder
from .decoder import Decoder
import tensorflow as tf
def Transformer(
    input_dim: int, 
    output_dim: int, 
    encoder_input_size: int = None,
    decoder_input_size: int = None,
    num_layers: int=1, 
    d_model: int=20, 
    num_heads: int=2,
    dff: int=64,
    dropout_rate: float=0.1,
    ) -> tf.keras.Model:
    """
    A custom TensorFlow model that implements the Transformer architecture.

    Args:
        input_dim (int): The size of the input.
        output_dim (int): The size of the target vocabulary.
        encoder_input_size (int): The size of the encoder input sequence.
        decoder_input_size (int): The size of the decoder input sequence.
        num_layers (int): The number of layers in the encoder and decoder.
        d_model (int): The dimensionality of the model.
        num_heads (int): The number of heads in the multi-head attention layer.
        dff (int): The dimensionality of the feed-forward layer.
        dropout_rate (float): The dropout rate.

    Returns:
        A TensorFlow Keras model.
    """
    inputs = [
        tf.keras.layers.Input(shape=(encoder_input_size,), dtype=tf.int64), 
        tf.keras.layers.Input(shape=(decoder_input_size,), dtype=tf.int64)
        ]
    
    encoder_input, decoder_input = inputs

    encoder = Encoder(num_layers=num_layers, d_model=d_model, num_heads=num_heads, dff=dff, input_dim=input_dim, dropout_rate=dropout_rate)(encoder_input)
    decoder = Decoder(num_layers=num_layers, d_model=d_model, num_heads=num_heads, dff=dff, output_dim=output_dim, dropout_rate=dropout_rate)(decoder_input, encoder)

    output = tf.keras.layers.Dense(1)(decoder)

    return tf.keras.Model(inputs=inputs, outputs=output)