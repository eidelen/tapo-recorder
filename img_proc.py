
import cv2    # pip install opencv-python
import numpy as np

def mean_square_error(img1, img2) -> float:
    '''
    Computes the mean square error of two opencv grayscale images.
    :param img1: Image 1
    :param img2: Image 2
    :return: MSE
    '''
    h1, w1 = img1.shape
    h2, w2 = img2.shape
    if h1 != h2 or w1 != w2:
        raise Exception('Dimension mismatch')

    diff_img = cv2.subtract(img1.astype('int64'), img2.astype('int64'))
    err = np.sum(diff_img ** 2)
    return err / (float(h1 * w1))

