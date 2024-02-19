import unittest
import numpy as np
import BioSigProc

from BioSigProc.biosigproc import (
    add_salt_and_pepper_noise,
    add_poisson_noise,
    add_uniform_noise,
    add_gaussian_noise,
)


class TestNoiseFunctions(unittest.TestCase):

    def setUp(self):
        self.signal = np.array([0.1, 0.3, 0.5, 0.7, 0.9])

    def test_add_salt_and_pepper_noise(self):
        noisy_signal = add_salt_and_pepper_noise(self.signal, salt_prob=0.2, pepper_prob=0.2)
        self.assertTrue(np.array_equal(noisy_signal, self.signal))

    def test_add_poisson_noise(self):
        noisy_signal = add_poisson_noise(self.signal, noise_lam=0.1)
        self.assertTrue(np.array_equal(noisy_signal, self.signal))

    def test_add_uniform_noise(self):
        noisy_signal = add_uniform_noise(self.signal, noise_level=0.2)
        self.assertTrue(np.array_equal(noisy_signal, self.signal))

    def test_add_gaussian_noise(self):
        noisy_signal = add_gaussian_noise(self.signal, noise_mean=0.1, noise_std=0.05)
        self.assertTrue(np.array_equal(noisy_signal, self.signal))


if __name__ == '__main__':
    unittest.main()
