import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

bins = np.arange(256).reshape(256, 1)


def draw_histogram(img):

    hist_item = cv.calcHist([img], [0], None, [256], [0, 256])
    for x, y in enumerate(hist_item):
        print(x, y)

    return y


img = cv.imread('img/case1.jpg', cv.IMREAD_COLOR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


line = draw_histogram(gray)

print(line)
