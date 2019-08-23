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
        self._matches_subset = self.filter_matches(matches, ratio)

    def get_filtered_matchs(self, ratio=0.75):
        return self._matches_subset

    def filter_matches(self, matches, ratio=0.75):
        filtered_matches = []
        for m, n in matches:
            if m.distance < ratio * n.distance:
                filtered_matches.append(m)
        return filtered_matches

    def find_homography(self):

        kp1 = []
        kp2 = []

        for match in self._matches_subset:
            kp1.append(self._drone_features[match.trainIdx])
            kp2.append(self._lidar_features[match.queryIdx])

        p1 = np.array([k.pt for k in kp1])
        p2 = np.array([k.pt for k in kp2])

        self._homography, self._status = cv2.findHomography(
            p1, p2, cv2.RANSAC, 5.0)

    def get_homography(self):
        return self._homography, self._status

    def draw_matches(self, drone_img, lidar_img, file_name):
        matchesMask = self._status.ravel().tolist()
        height, width = drone_img.shape
        pts = np.float32([[0, 0], [0, height - 1], [width - 1,
                                                    height - 1], [width - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, self._homography)
        lidar_img = cv2.polylines(
            lidar_img, [
                np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        draw_params = dict(matchColor=(0, 0, 255),  # draw matches in blue color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img3 = cv2.drawMatches(
            lidar_img,
            self._lidar_features,
            drone_img,
            self._drone_features,
            self._matches_subset,
            None,
            **draw_params)
        plt.imshow(img3, 'gray'), plt.show()
        cv2.imwrite(file_name, img3)
