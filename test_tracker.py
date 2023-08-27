import unittest
import numpy as np
import img_proc as ip

class TapoTrackerTest(unittest.TestCase):

    def test_mse(self):
        black_image = np.zeros((200, 100), np.uint8)
        white_image = np.ones((200, 100), np.uint8)
        white_image.fill(255)
        self.assertAlmostEqual(ip.mean_square_error(white_image, black_image), 255**2)
        self.assertAlmostEqual(ip.mean_square_error(black_image, white_image), 255**2)
        self.assertAlmostEqual(ip.mean_square_error(black_image, black_image), 0.0)
        self.assertAlmostEqual(ip.mean_square_error(white_image, white_image), 0.0)

    def test_mse_raise(self):
        black_image = np.zeros((200, 101), np.uint8)
        white_image = np.ones((200, 100), np.uint8)
        with self.assertRaises(Exception):
            ip.mean_square_error(white_image, black_image)



