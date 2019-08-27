import cv2
import numpy as np
from matplotlib import pyplot as plt


class Matcher:

    def __init__(
            self,
            drone_features,
            drone_descs,
            lidar_features,
            lidar_descs):
        FLANN_INDEX_KDTREE = 1
        flann_params = dict(algorithm=FLANN_INDEX_KDTREE,
                            trees=5)
        self.matcher = cv2.FlannBasedMatcher(flann_params, {})

        self._drone_features = drone_features
        self._drone_descs = drone_descs

        self._lidar_features = lidar_features
        self._lidar_descs = lidar_descs

    def extract_match(self, ratio=0.75):
        matches = self.matcher.knnMatch(
            self._lidar_descs, trainDescriptors=self._drone_descs, k=2)
        self._good_matches = self.find_good_matches(matches, ratio)

    def get_good_matchs(self):
        return self._good_matches

    def find_good_matches(self, matches, ratio=0.75):
        good_matches = []
        for m, n in matches:
            if m.distance < ratio * n.distance:
                good_matches.append(m)
        return good_matches

    def draw_matches(
            self,
            src_drone_img,
            src_lidar_img,
            matchesMask=None,
            homography=None):
        drone_img = src_drone_img.copy()
        lidar_img = src_lidar_img.copy()

        if(matchesMask is not None):
            matchesMask = matchesMask.ravel().tolist()

        if(homography is not None):
            height, width = drone_img.shape
            pts = np.float32([[0, 0], [0, height - 1], [width - 1,
                                                        height - 1], [width - 1, 0]]).reshape(-1, 1, 2)

            dst = cv2.perspectiveTransform(pts, homography)
            lidar_img = cv2.polylines(
                lidar_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        draw_params = dict(matchColor=(0, 0, 255),  # draw matches in blue
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        matching_img = cv2.drawMatches(
            lidar_img,
            self._lidar_features,
            drone_img,
            self._drone_features,
            self._good_matches,
            None,
            **draw_params)

        plt.imshow(matching_img, 'gray')
        plt.show()
