#!/usr/bin/env python3
"""
DIRESA loss classes/functions
:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

import tensorflow as tf
import tensorflow_probability as tfp
from keras.losses import Loss


class KLLoss(Loss):
    """
    KL weighted loss class
    KL weight is annealed by KLAnnealingCallback
    """
    def __init__(self, kl_weight):
        """
        :param kl_weight: tensorflow variable with initial KL loss weight
        """
        super().__init__()
        self.kl_weight = kl_weight

    def call(self, _, z_mean_var):
        """
        :param _: not used (loss functions need 2 params: the true and predicted values)
        :param z_mean_var: list with mean and ln of the variance of the distribution
        :return: weighted KL loss
        """
        z_mean, z_log_var = tf.split(z_mean_var, num_or_size_splits=2, axis=1)
        loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        return self.kl_weight * tf.reduce_mean(loss, axis=-1)


class LatentCovLoss(Loss):
    """
    Latent covariance loss class
    Latent covariance weight is annealed by AnnealingCallback
    """
    def __init__(self, cov_weight):
        """
        :param cov_weight: tensorflow variable with initial covariance loss weight
        """
        super().__init__()
        self.cov_weight = cov_weight

    def call(self, _, latent):
        """
        :param _: not used (loss functions need 2 params: the true and predicted values)
        :param latent: batch of latent vectors
        :return: weighted covariance loss
        """
        cov = tf.math.abs(tfp.stats.covariance(latent))
        cov_square = tf.math.multiply(cov, cov)
        nbr_of_cov = tf.shape(latent)[-1] * (tf.shape(latent)[-1] - 1)
        cov_loss = (tf.math.reduce_sum(cov_square) - tf.linalg.trace(cov_square)) / tf.cast(nbr_of_cov, "float32")
        return self.cov_weight * cov_loss


def mae_dist_loss(_, distances):
    """
    Absolute Error between original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute errors
    """
    ae = tf.math.abs(distances[:, 0] - distances[:, 1])
    return ae


def male_dist_loss(_, distances):
    """
    Absolute Error between logarithm of original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute logarithmic errors
    """
    ale = tf.math.abs(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return ale


def mape_dist_loss(_, distances):
    """
    Absolute Percentage Error between original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of absolute percentage errors
    """
    epsilon = 1e-8
    ape = tf.math.abs((distances[:, 0] - distances[:, 1]) / (distances[:, 0] + epsilon))
    return ape


def mse_dist_loss(_, distances):
    """
    Squared Error between original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared errors
    """
    se = tf.math.square(distances[:, 0] - distances[:, 1])
    return se


def msle_dist_loss(_, distances):
    """
    Squared Error between logarithm of original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: batch of squared logarithmic errors
    """
    sle = tf.math.square(tf.math.log1p(distances[:, 0]) - tf.math.log1p(distances[:, 1]))
    return sle


def corr_dist_loss(_, distances):
    """
    Correlation loss between original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient
    """
    cov = tfp.stats.covariance(distances)
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


def corr_log_dist_loss(_, distances):
    """
    Correlation loss between logarithm of original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient (of logarithmic distances)
    """
    cov = tfp.stats.covariance(tf.math.log1p(distances))
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


def loc_corr_dist_loss(_, distances):
    """
    Correlation loss between original and latent distances with location parameter
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - correlation coefficient (of 50% closest distances in latent space)
    """
    location_param = tf.cast(tf.shape(distances)[0], tf.int32) // 2
    distances = tf.gather(distances, tf.argsort(distances[:, 1]))  # sort by latent distance
    distances = distances[:location_param]  # take only closest
    cov = tfp.stats.covariance(distances)
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


def spear_dist_loss(_, distances):
    """
    Spearman correlation loss between original and latent distances
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: 1 - Spearman correlation coefficient
    """
    index0 = tf.argsort(distances[:, 0])
    index1 = tf.argsort(distances[:, 1])
    cov = tfp.stats.covariance(tf.stack((index0, index1), axis=-1))
    cov_sqrt = tf.math.sqrt(tf.math.abs(cov))
    return 1 - cov[0, 1] / (cov_sqrt[0, 0] * cov_sqrt[1, 1])


def canberra_dist_loss(_, distances):
    """
    Canberra distance loss with location parameter
    https://github.com/richardARPANET/mlpy/blob/master/mlpy/canberra/c_canberra.c
    :param _: not used (loss functions need 2 params: the true and predicted values)
    :param distances: batch of original and latent distances between twins
    :return: Canberra distance (of 50% closest distances in latent space)
    """
    location_param = tf.cast(tf.shape(distances)[0], tf.int32) // 2
    distances = tf.gather(distances, tf.argsort(distances[:, 1]))  # sort by latent distance
    # indices of the sort of the 2 columns (first is [0,1,2,3...] )
    # top those with location_param + 1
    index0 = tf.math.minimum(tf.argsort(distances[:, 0]) + 1, tf.constant(location_param + 1))
    index1 = tf.math.minimum(tf.argsort(distances[:, 1]) + 1, tf.constant(location_param + 1))
    # canberra distance of the 2 indices
    return tf.math.reduce_sum(tf.math.abs(index0 - index1) / (index0 + index1))
