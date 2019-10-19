import cv2
import numpy as np
import matplotlib.pyplot as plt


class Preprocessor:

    def __init__(self, drone_img, pcl_img):
        self.drone_img = drone_img
        self.pcl_img = pcl_img

        self.processed_drone_img = None
        self.processed_pcl_img = None
        self.processed_drone_mask = None
        self.processed_pcl_mask = None
        self.masked_drone_img = None
        self.masked_pcl_img = None

    def preprocessing(self):
        self.processed_drone_img = self._drone_img_preprocessing()
        self.processed_pcl_img = self._pcl_img_preprocessing()
        self.processed_drone_mask = self._process_drone_mask()
        self.processed_pcl_mask = self._process_pcl_mask()
        self.masked_drone_img = self._get_masked_img(
            self.processed_drone_img, self.processed_drone_mask)
        self.masked_pcl_img = self._get_masked_img(
            self.processed_pcl_img, self.processed_pcl_mask)

    def _get_masked_img(self, img, mask):
        masked_img = cv2.bitwise_and(img, mask, None)
        return masked_img

    def _drone_img_preprocessing(self):
        # TODO
        return cv2.cvtColor(self.drone_img, cv2.COLOR_BGR2GRAY)
        # return cv2.GaussianBlur(
        #    cv2.cvtColor(
        #        self.drone_img, cv2.COLOR_BGR2GRAY), (5, 5), 0)

    def _process_drone_mask(self):
        return cv2.imread('/media/visionnoob/dataset/Sample Data (2)/ex1/CASE1_1/mask.bmp', cv2.IMREAD_GRAYSCALE)

    def _process_pcl_mask(self):
        plc_img = self.processed_pcl_img
        plc_img[plc_img == 224] = 0
        ret, mask = cv2.threshold(plc_img, 1, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)

        mask_ero = cv2.erode(mask, kernel, iterations=7)
        contours = cv2.findContours(
            mask_ero, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        max_idx = 0
        max_len = 0

        for i in range(len(contours[1])):
            c = contours[1][i]
            if(max_len < len(c)):
                max_len = len(c)
                max_idx = i

        selected_contour = contours[1][max_idx].reshape(1, -1, 2)

        mask2 = np.zeros(mask_ero.shape, np.uint8)
        mask2 = cv2.fillPoly(mask2, selected_contour, color=[255])

        mask3 = cv2.dilate(mask2, kernel, iterations=5)
        return mask3

    def _pcl_img_preprocessing(self):
        gray_img = cv2.cvtColor(self.pcl_img, cv2.COLOR_BGR2GRAY)
        return cv2.medianBlur(gray_img, 3)

    def get_processed_imgs(self):

        return {'processed_drone_img': self.processed_drone_img,
                'processed_pcl_img': self.processed_pcl_img,
                'processed_drone_mask': self.processed_drone_mask,
                'processed_pcl_mask': self.processed_pcl_mask,
                'masked_drone_img': self.masked_drone_img,
                'masked_pcl_img': self.masked_pcl_img
                }
