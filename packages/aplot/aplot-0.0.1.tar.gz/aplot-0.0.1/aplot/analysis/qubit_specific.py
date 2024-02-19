import typing as _t

import numpy as np


def correct_for_delay(
    freqs: np.ndarray, z: np.ndarray, delay: _t.Optional[float] = None
) -> _t.Tuple[np.ndarray, np.ndarray]:
    """Correct z with given delay.
    Algo: corrected_z = np.exp(-1j*delay*freqs)*z
    Return: freqs, corrected_z"""
    if delay is None:
        # https://github.com/UlysseREGLADE/abcd_rf_fit#3-estimation-of-the-electrical-delay
        delay = np.sum(np.angle(z[1:] / z[:-1]) / np.diff(freqs)) / len(z) / 2 / np.pi
    corrected = np.exp(-1j * 2 * np.pi * delay * freqs) * z
    return freqs, corrected * np.exp(-1j * np.mean(np.unwrap(np.angle(corrected), axis=-1)))


def get_formatted_data_from_two_tone(
    voltages: np.ndarray,
    freqs: _t.Union[_t.Tuple[np.ndarray, np.ndarray], np.ndarray],
    z: np.ndarray,
):
    """


    Args:
        voltages (np.ndarray): An array of voltage values corresponding to measurements.
        freqs (Union[Tuple[np.ndarray, np.ndarray], np.ndarray]):
            Either a tuple containing two arrays of frequencies (IF and LO) or a single array
            of frequencies.
        z (np.ndarray): An array of impedance measurements.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing two arrays:
            - freqs (np.ndarray): The sorted and combined frequency values.
            - z (np.ndarray): The data reshaped and sorted according to the frequency values.

    """
    if isinstance(freqs, tuple):
        lo_freqs, if_freqs = freqs
        ifs, los = np.meshgrid(if_freqs, lo_freqs)
        # los, ifs = np.meshgrid(lo_freqs, if_freqs)
        freqs = (los + ifs).flatten()
    z = z.reshape((len(voltages), len(freqs)))
    sorted_freqs = np.argsort(freqs)
    freqs = freqs[sorted_freqs]
    z = z[:, sorted_freqs]
    return voltages, freqs, z
