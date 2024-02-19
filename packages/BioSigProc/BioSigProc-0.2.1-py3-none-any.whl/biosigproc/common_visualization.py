# common_visualization.py
"""
Module for common signal visualization.

This module provides functions for plotting various signals, offering options
to customize the appearance of the plot and save it to a file.

Functions:
- plot_signal: Plot a signal.
- plot_fft: Plot the Fourier Transform of a signal.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_signal(signal, fs=None, xlim=None, ylim=None, title=None, show_fig=True, file_path=None, figsize=(20, 8),
                color='blue'):
    """
    Plot signal.

    Parameters:
        - signal (numpy.ndarray): The signal data.
        - fs (float, optional): Sampling frequency in Hz (default: None).
        - xlim (tuple, optional): x-axis limits for the plot (default: None).
        - ylim (tuple, optional): y-axis limits for the plot (default: None).
        - title (str, optional): Title of the plot (default: None).
        - show_fig (bool, optional): Whether to display the figure (default: True).
        - file_path (str, optional): File path to save the figure (default: None).
        - figsize (tuple, optional): Figure size (default: (20, 8)).
        - color (str, optional): Matplotlib line color (default: 'blue').

    Returns:
        None
    """

    if not isinstance(signal, np.ndarray):
        raise TypeError("`signal` must be a numpy array.")

    fig, ax = plt.subplots(figsize=figsize)

    if fs is not None:
        time = np.arange(0, len(signal) * 1 / fs, 1 / fs)
        ax.set_xlabel('Time [s]')
    else:
        time = np.arange(0, len(signal))

    if xlim:
        ax.set_xlim(*xlim)

    if ylim:
        ax.set_ylim(*ylim)

    ax.plot(time, signal, color=color)

    ax.set_ylabel('PPG Signal')
    if title:
        ax.set_title(title)

    if file_path:
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(file_path)
            print(f"Figure saved to {file_path}")
        except Exception as e:
            print(f"Error saving figure: {e}")

    if show_fig:
        plt.show()
    plt.close()

    return


def plot_fft(signal, fs, xlim=None, ylim=None, title=None, show_fig=True, file_path=None, figsize=(20, 8),
             color='blue'):
    """
    Plot the Fourier Transform of a signal.

    Parameters:
        - signal (numpy.ndarray): The input signal.
        - fs (float): Sampling frequency.
        - xlim (tuple, optional): x-axis limits for the plot (default: None).
        - ylim (tuple, optional): y-axis limits for the plot (default: None).
        - title (str, optional): Title of the plot (default: None).
        - show_fig (bool, optional): Whether to display the figure (default: True).
        - file_path (str, optional): File path to save the figure (default: None).
        - figsize (tuple, optional): Figure size (default: (20, 8)).
        - color (str, optional): Matplotlib line color (default: 'blue').

    Returns:
        None
    """

    # Compute the Fourier Transform of the signal
    signal_fft = np.fft.fftshift(np.fft.fft(signal))
    frequency_axis = np.fft.fftshift(np.fft.fftfreq(len(signal), d=1 / fs))

    # Check if the input signal is a numpy array
    if not isinstance(signal, np.ndarray):
        raise TypeError("`signal` must be a numpy array.")

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the Fourier Transform
    ax.plot(frequency_axis[len(frequency_axis) // 2:], np.abs(signal_fft[len(frequency_axis) // 2:]),color=color)

    # Set x-axis limits if provided
    if xlim:
        ax.set_xlim(*xlim)

    # Set y-axis limits if provided
    if ylim:
        ax.set_ylim(*ylim)

    # Set x and y axis labels
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')

    # Set plot title if provided
    if title:
        ax.set_title(title)

    # Save the figure to a file if file_path is provided
    if file_path:
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(file_path)
            print(f"Figure saved to {file_path}")
        except Exception as e:
            print(f"Error saving figure: {e}")

    # Display the plot if show_fig is True
    if show_fig:
        plt.show()
    plt.close()

    return



