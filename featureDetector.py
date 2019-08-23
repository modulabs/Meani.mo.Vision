import cv2


class FeatureDetector:

    def __init__(self, drone_img, algorithm1, lidar_img, algorithm2):

        self._init_detector_funcs()

        self._drone_img_detector = self._load_detector(algorithm1)
        self._lidar_img_detector = self._load_detector(algorithm2)

        self._drone_img = drone_img
        self._lidar_img = lidar_img

    def _init_detector_funcs(self):
        self._detectors = {
            "SIFT": cv2.xfeatures2d.SIFT_create
        }

    def _load_detector(self, algorithm):
        return self._detectors[algorithm]()

    def compute_features_and_descriptor(self):
        self.drone_img_features, self.drone_img_descs = self._drone_img_detector.detectAndCompute(
            self._drone_img, None)
        self.lidar_img_features, self.lidar_img_descs = self._lidar_img_detector.detectAndCompute(
            self._lidar_img, None)

    def get_feature_and_descriptor(self, img_type):
        if img_type == "drone":
            return self.drone_img_features, self.drone_img_descs
        elif img_type == "lidar":
            return self.lidar_img_features, self.lidar_img_descs
