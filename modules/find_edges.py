import numpy as np
import cv2
from scipy.signal import convolve2d
import math
from scipy.ndimage import gaussian_filter

def gaussian_smoothing(img, sigma):
    img_gaus = gaussian_filter(img, sigma)
    return (img_gaus)


def gradient(img):
    kernel_sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    kernel_sobel_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    sobel_x = convolve2d(img / 255, kernel_sobel_x)
    sobel_y = convolve2d(img / 255, kernel_sobel_y)

    magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    direction = (np.arctan(sobel_y / (sobel_x + 0.0001))) + (math.pi / 2)

    return (magnitude, direction)


def quantitizer(direction):
    direction_1 = np.array([direction < (math.pi / 8)]).astype(int)
    direction_1 = direction_1 * (0)

    direction_2 = np.array([(direction < 3 * math.pi / 8) & (direction >= (math.pi / 8))])
    direction_2 = direction_2 * (math.pi / 4)

    direction_3 = np.array([(direction < 5 * math.pi / 8) & (direction >= (3 * math.pi / 8))])
    direction_3 = direction_3 * (math.pi / 2)

    direction_4 = np.array([(direction < 7 * math.pi / 8) & (direction >= (5 * math.pi / 8))])
    direction_4 = direction_4 * (3 * math.pi / 4)

    direction_5 = np.array([(direction >= (7 * math.pi / 8))])
    direction_5 = direction_5 * 0

    direction_final = direction_1 + direction_2 + direction_3 + direction_4 + direction_5

    direction_final = np.array(direction_final)[0]

    return (direction_final)


def non_maximum_suppression(g_magnitude, g_dir):
    new_g_magnitude = np.copy(g_magnitude)

    shape = g_dir.shape

    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            x = 0
            y = 0
            direction = g_dir[i][j]

            if (direction == 0):
                x1 = 0
                y1 = 1
                x2 = 0
                y2 = -1
            elif (direction == math.pi / 4):
                x1 = 1
                y1 = -1
                x2 = -1
                y2 = 1
            elif (direction == math.pi / 2):
                x1 = -1
                y1 = 0
                x2 = 1
                y2 = 0
            elif (direction == 3 * math.pi / 4):
                x1 = 1
                y1 = 1
                x2 = -1
                y2 = -1
            else:
                print('ERROR')

            neigh1 = g_magnitude[i + x1][j + y1]
            neigh2 = g_magnitude[i + x2][j + y2]
            mag = g_magnitude[i][j]

            if (neigh1 >= mag or neigh2 >= mag):
                new_g_magnitude[i][j] = 0
    return (new_g_magnitude)


def double_thresholding(mag, thresh_lo, thresh_hi):
    new_mag = np.copy(mag)
    max_grad = mag.max()
    low_trheshold = max_grad * thresh_lo
    high_trheshold = max_grad * thresh_hi
    shape = mag.shape
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            magij = mag[i][j]
            if (magij < low_trheshold):
                new_mag[i][j] = 0
            elif ((magij < high_trheshold) and (magij >= low_trheshold)):
                new_mag[i][j] = 1
            else:
                new_mag[i][j] = 2
    return (new_mag)


def connect_edge(mag):
    new_mag = np.copy(mag) * 0
    shape = new_mag.shape
    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            if (mag[i][j] == 2):
                new_mag[i][j] = 1
            if (mag[i][j] == 0):
                new_mag[i][j] = 0
            else:
                n1 = mag[i - 1][j - 1]
                n2 = mag[i][j - 1]
                n3 = mag[i + 1][j - 1]
                n4 = mag[i - 1][j]
                n5 = mag[i + 1][j]
                n6 = mag[i - 1][j + 1]
                n7 = mag[i][j + 1]
                n8 = mag[i + 1][j + 1]

                if (n1 == 2 or n2 == 2 or n3 == 2 or n4 == 2 or n5 == 2 or n6 == 2 or n8 == 2):
                    new_mag[i][j] = 1
                else:
                    new_mag[i][j] = 0
    return new_mag


def canny_edge_detector(img, sigma, thresh_lo=0.1, thresh_hi=0.2):
    """
    The Canny edge detector.

    Inputs:
        img              The input image
        thresh_lo        The fraction of the maximum gradient magnitude which will
                         be considered the lo threshold.
        thresh_hi        The fraction of the maximum gradient magnitude which will
                         be considered the hi threshold. Ideally should be 2x to 3x
                         thresh_lo.

    Outputs:
        edge_img         A binary image, with pixels lying on edges marked with a 1,
                         and others with a 0.
    """

    ##1

    filtered_img = gaussian_smoothing(img, sigma)

    ##2
    (mag, direction) = gradient(filtered_img)
    ##3_1
    direction = quantitizer(direction)
    ##3_1
    mag = non_maximum_suppression(mag, direction)
    ##4
    mag = double_thresholding(mag, thresh_lo, thresh_hi)
    ##5
    mag = connect_edge(mag)
    return mag


def find_edges(masked,sigma=1, thresh_lo=0.2, thresh_hi=0.5):
    edges_mask = canny_edge_detector(masked, sigma, thresh_lo, thresh_hi)
    edges = np.nonzero(edges_mask)

    res = [[], []]
    for i in zip(edges[0], edges[1]):
        res[0].append(i[0])
        res[1].append(i[1])

    return (np.array(res))