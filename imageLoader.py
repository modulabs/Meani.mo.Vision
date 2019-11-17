import cv2
import os
import logging


class ImageLoader:

    def __init__(self):
        self.img = None

    def get_img(self):
        return self.img

    def load_img(self, path):
        try:
            img = cv2.imread(path)
        except Exception as e:
            logging.error("{}".format(e))
            raise e
        else:
            self.img = img
