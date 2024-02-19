# common_utils.py
"""
Module for common signal processing.

This module provides functions for processing various signals.

Functions:
- add_salt_and_pepper_noise : Add salt and pepper noise to a signal.
- add_poisson_noise : Add Poisson noise to a normalized signal.
- add_uniform_noise : Add uniform noise to a signal.
- add_gaussian_noise : Add gaussian noise to a signal.
- add_noise : Add noise to the input signal based on the specified noise type.
-
-
"""

import numpy as np
import pywt


def add_salt_and_pepper_noise(signal, salt_prob=0.001, pepper_prob=0.001):
    """
    Add salt and pepper noise to a signal.

    Parameters:
    - signal (numpy.ndarray): Input signal.
    - salt_prob (float): Probability of adding salt noise (default: 0.01).
    - pepper_prob (float): Probability of adding pepper noise (default: 0.01).

    Returns:
    - numpy.ndarray: Signal with salt and pepper noise.
    """
    noisy_signal = np.copy(signal)

    # Add salt noise
    salt_mask = np.random.rand(*signal.shape) < salt_prob
    noisy_signal[salt_mask] = np.max(signal)

    # Add pepper noise
    pepper_mask = np.random.rand(*signal.shape) < pepper_prob
    noisy_signal[pepper_mask] = np.min(signal)

    return noisy_signal


def add_poisson_noise(signal, noise_lam=0.02):
    """
    Add Poisson noise to a normalized signal.

    Parameters:
    - signal(numpy array): input signal normalized between 0 and 1
    - noise_lam (float): Expected number of events occurring in a fixed-time interval

    Returns:
    - noisy_signal: numpy array, signal with added Poisson noise, still normalized between 0 and 1
    """
    noisy_signal = np.copy(signal)

    # Generate Poisson noise scaled by 0.05 to control the intensity
    poisson_noise = 0.1 * np.random.poisson(lam=noise_lam, size=len(signal))

    noisy_signal += poisson_noise

    return noisy_signal


def add_uniform_noise(signal, noise_level=0.01):
    """
    Add uniform noise to a signal.

    Parameters:
    - signal: numpy array, input signal
    - noise_level: float, magnitude of uniform noise (default is 0.1)

    Returns:
    - noisy_signal: numpy array, signal with added uniform noise
    """
    noisy_signal = np.copy(signal)
    uniform_noise = np.random.uniform(-noise_level, noise_level, len(signal))
    noisy_signal += uniform_noise
    return noisy_signal


def add_gaussian_noise(signal, noise_mean=0, noise_std=0.05):
    """
    Adds Gaussian noise to a signal.

    Parameters:
    - signal: numpy array, input signal
    - noise_mean: float, mean of the Gaussian noise (default is 0)
    - noise_std: float, standard deviation of the Gaussian noise (default is 0.05)

    Returns:
    - noisy_signal: numpy array, signal with added Gaussian noise
    """
    noisy_signal = np.copy(signal)
    gaussian_noise = np.random.normal(loc=noise_mean, scale=noise_std, size=len(signal))
    noisy_signal += gaussian_noise
    return noisy_signal


def add_noise(signal, noise_type='gaussian', noise_params=None):
    """
    Add noise to the input signal based on the specified noise type.

    Parameters:
    - signal (numpy.ndarray): The input signal.
    - noise_type (str): The type of noise to be added. Supported types: 'gaussian', 'salt_and_pepper', 'uniform', 'poisson'.
    - noise_params (dict): Parameters for controlling the characteristics of the noise.
    Returns:
    - numpy.ndarray: The noisy signal with added random noise.
    """
    if noise_type == 'gaussian':
        # Add Gaussian noise to the signal
        noisy_signal = add_gaussian_noise(signal, noise_params.get('mean', 0), noise_params.get('std', 0.05))
    elif noise_type == 'salt_and_pepper':
        # Add salt and pepper noise to the signal
        noisy_signal = add_salt_and_pepper_noise(signal, noise_params.get('salt_prob', 0.01),
                                                 noise_params.get('pepper_prob', 0.01))
    elif noise_type == 'uniform':
        # Add uniform noise to the signal
        noisy_signal = add_uniform_noise(signal, noise_params.get('level', 0.1))
    elif noise_type == 'poisson':
        # Add Poisson noise to the signal
        noisy_signal = add_poisson_noise(signal, noise_params.get('noise_lam', 0.02))
    else:
        raise ValueError(f"Unsupported noise type: {noise_type}")

    return noisy_signal


def wavelet_signal(signal, wavelet='db4', level=4, fs=None):
    """
    Perform wavelet decomposition on a given signal.

    Parameters:
    - signal (numpy.ndarray): Input signal to be decomposed.
    - wavelet (str): Wavelet function to be used (default: 'db4').
    - level (int): Decomposition level (default: 4).
    - fs (float, optional): Sampling frequency in Hz (default: None).

    Returns:
    - list: List of wavelet coefficients at each decomposition level.
    """
    # Display frequency information if sampling frequency is provided
    if fs:
        for i in range(1, level + 1):
            print(f"coefficient D{i} and corresponding frequencies are {fs / (2 ** i)}-{fs / (2 ** (i - 1))} Hz")
        print(f"coefficient A{level} and corresponding frequencies are {0} - {fs / (2 ** level)} Hz")

    try:
        # Perform wavelet decomposition
        coeffs = pywt.wavedec(signal, wavelet, level=level)
    except ValueError as e:
        print(f"Error in wavelet decomposition: {e}")
        return None

    return coeffs
