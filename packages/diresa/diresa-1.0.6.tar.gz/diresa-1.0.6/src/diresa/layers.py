#!/usr/bin/env python3
"""
DIRESA custom layer classes
:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import keras
import tensorflow as tf
from keras import layers

class Sampling(layers.Layer):
    """
        Samples from distribution with z_mean and z_log_var
        https://keras.io/examples/generative/vae/
    """

    def __init__(self, name=None, **kwargs):
        super(Sampling, self).__init__(name=name, **kwargs)

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    def get_config(self):
        cfg = super().get_config()
        return cfg


class DistLayer(keras.layers.Layer):
    """
        Calculates distances between the 2 inputs and between the 2 outputs of a twin model
    """

    def __init__(self, name=None, **kwargs):
        super(DistLayer, self).__init__(name=name, **kwargs)

    def call(self, x1, x2, y1, y2):
        dist1 = tf.math.reduce_sum(tf.math.square(x1 - x2), axis=range(1, tf.rank(x1)))  # sum over all dims, except 0
        dist2 = tf.math.reduce_sum(tf.math.square(y1 - y2), axis=range(1, tf.rank(y1)))  # sum over all dims, except 0
        return tf.stack((dist1, dist2), axis=-1)

    def get_config(self):
        cfg = super().get_config()
        return cfg


class MaskLayer(keras.layers.Layer):
    """
        MaskLayer as in Royen et al. (2021) - MaskLayer: Enabling scalable deep learning solutions by training embedded feature sets
    """

    def __init__(self, inference_units=0, name=None, **kwargs):
        super(MaskLayer, self).__init__(name=name, **kwargs)
        self.units = None
        self.inference_units = inference_units

    def build(self, input_shape):
        self.units = input_shape[-1]

    def call(self, inputs, training):
        if training:
            size = tf.experimental.numpy.random.randint(self.units) + 1
            mask = tf.concat(
                [tf.ones([size], dtype="float32"),
                 tf.zeros([self.units - size], dtype="float32")], 0)
            inputs = tf.multiply(inputs, mask)
            inputs = tf.scalar_mul(tf.cast(self.units / size, dtype="float32"), inputs)
        else:
            if self.inference_units != 0:
                mask = tf.concat(
                    [tf.ones([self.inference_units], dtype="float32"),
                     tf.zeros([self.units - self.inference_units], dtype="float32")], 0)
                inputs = tf.multiply(inputs, mask)
        return inputs

    def get_config(self):
        cfg = super().get_config()
        return cfg