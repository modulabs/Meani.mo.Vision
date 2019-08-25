import cv2


class Preprocessor:

    def __init__(self, drone_img, lidar_img):
        self.drone_img = drone_img
        self.lidar_img = lidar_img

        self.processed_drone_img = None
        self.processed_lidar_img = None

    def preprocessing(self):
        self.processed_drone_img = self._drone_img_preprocessing()
        self.processed_lidar_img = self._lidar_img_preprocessing()

    def _drone_img_preprocessing(self):
        # TODO
        return cv2.GaussianBlur(
            cv2.cvtColor(
                self.drone_img, cv2.COLOR_BGR2GRAY), (5, 5), 0)

    def _lidar_img_preprocessing(self):
        # TODO
        return cv2.medianBlur(cv2.cvtColor(
            self.lidar_img, cv2.COLOR_BGR2GRAY), 5)

    def get_processed_imgs(self):
        return self.processed_drone_img, self.processed_lidar_img
