import cv2
import numpy as np
import matplotlib.pyplot as plt

def mask(img, hmin, smin, vmin, hmax, smax, vmax):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    threshold_down = (hmin, smin, vmin)
    threshold_up = (hmax, smax, vmax)
    masked = cv2.inRange(hsv_img, threshold_down, threshold_up)
    return masked


def crop_and_resize_mask(masked):
    masked = masked.astype("float32")
    masked = cv2.resize(masked, (256, 256))
    pad = 15
    masked = masked[pad:masked.shape[0] - pad, pad:masked.shape[1] - pad]
    masked = np.pad(masked, (pad, pad), 'constant', constant_values=(masked.max(), masked.max()))
    masked = masked / masked.max()

    return masked


def get_mask(img, hmin, smin, vmin, hmax, smax, vmax):
    masked = mask(img, hmin, smin, vmin, hmax, smax, vmax)
    return crop_and_resize_mask(masked)
