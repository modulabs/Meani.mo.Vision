import cv2
import numpy as np


class Preprocessor:

    def __init__(self, drone_img, pcl_img):
        self.drone_img = drone_img
        self.pcl_img = pcl_img

        self.processed_drone_img = None
        self.processed_pcl_img = None
        self.processed_pcl_mask = None
        self.masked_pcl_img = None

    def preprocessing(self):
        self.processed_drone_img = self._drone_img_preprocessing()
        self.processed_pcl_img = self._pcl_img_preprocessing()
        self.processed_pcl_mask = self._process_pcl_mask()
        self.masked_pcl_img = self._process_masked_pcl_img()

    def _process_masked_pcl_img(self):
        masked_pcl_img = cv2.bitwise_and(
            self.processed_pcl_img, self.processed_pcl_mask, None)
        return masked_pcl_img

    def _drone_img_preprocessing(self):
        # TODO
        return cv2.cvtColor(self.drone_img, cv2.COLOR_BGR2GRAY)
        # return cv2.GaussianBlur(
        #    cv2.cvtColor(
        #        self.drone_img, cv2.COLOR_BGR2GRAY), (5, 5), 0)

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

        print(max_len, max_idx)
        selected_contour = contours[1][max_idx].reshape(1, -1, 2)

        mask2 = np.zeros(mask_ero.shape, np.uint8)
        mask2 = cv2.fillPoly(mask2, selected_contour, color=[255])

        mask3 = cv2.dilate(mask2, kernel, iterations=5)

        return mask3

    def _pcl_img_preprocessing(self):
        gray_img = cv2.cvtColor(self.pcl_img, cv2.COLOR_BGR2GRAY)
        return cv2.medianBlur(gray_img, 5)

    def get_processed_imgs(self):
        return self.processed_drone_img, self.processed_pcl_img, self.masked_pcl_img, self.processed_pcl_mask
