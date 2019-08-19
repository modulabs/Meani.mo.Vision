import cv2
import os
import logging

class ImageLoader:

    def __init__(self,drone_img_path,lidar_img_path):
        self.drone_img_path = drone_img_path
        self.lidar_img_path = lidar_img_path
        self.drone_img = None
        self.lidar_img = None

    def load_imgs(self):
        self.drone_img = self.load_img(self.drone_img_path)
        self.lidar_img = self.load_img(self.lidar_img_path)

    def get_imgs(self):
        return self.drone_img,self.lidar_img


    def load_img(self,path):
        try:
            img = cv2.imread(path)
        except Exception as e:
            logging.error("{}".format(e))
            raise e
        else:
            return img