import math
import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg
from imageLoader import ImageLoader as Loader
from preprocessor import Preprocessor
from featureExtractor import FeatureExtractor
from matcher import Matcher


def registrate(drone_img_ori, lidar_img_ori):

    # Preprocess Images
    img_preprocessor = Preprocessor(drone_img_ori, lidar_img_ori)
    img_preprocessor.preprocessing()
    drone_img, lidar_img = img_preprocessor.get_processed_imgs()

    # Extract Features
    drone_feature_extractor = FeatureExtractor(drone_img, "SIFT")
    lidar_feature_extractor = FeatureExtractor(lidar_img, "SIFT")

    drone_feature_extractor.compute()
    lidar_feature_extractor.compute()

    drone_features, drone_descs = drone_feature_extractor.get_features_and_descriptors()
    lidar_features, lidar_descs = lidar_feature_extractor.get_features_and_descriptors()

    # Find Matching
    matcher = Matcher(drone_features, drone_descs, lidar_features, lidar_descs)
    matcher.extract_match()
    good_matchs = matcher.get_good_matchs()

    # Find Homography
    homography, status = find_homography(
        drone_features, lidar_features, good_matchs)

    # Show matches
    matcher.draw_matches(drone_img, lidar_img, status, homography)
    # matcher.draw_matches(drone_img, lidar_img, None, homography)
    # matcher.draw_matches(drone_img, lidar_img)

    result_image_width = drone_img_ori.shape[1] + lidar_img_ori.shape[1]
    result_image_height = drone_img_ori.shape[0]

    # Warp and Image Blending
    registated_image = cv2.warpPerspective(
        drone_img_ori, homography, (result_image_width, result_image_height))

    image_roi = registated_image[0:lidar_img_ori.shape[0],
                                 0:lidar_img_ori.shape[1]]
    image_roi = 0.5 * image_roi + lidar_img_ori * 0.5

    registated_image[0:lidar_img_ori.shape[0],
                     0:lidar_img_ori.shape[1]] = image_roi

    plt.imshow(registated_image, 'gray')
    plt.show()

    return registated_image


def find_homography(features1, features2, matches):
    key_points1 = []
    key_points2 = []

    for match in matches:
        key_points1.append(features1[match.trainIdx])
        key_points2.append(features2[match.queryIdx])

    src_points = np.array([k.pt for k in key_points1])
    dst_points = np.array([k.pt for k in key_points2])

    homography, status = cv2.findHomography(
        src_points, dst_points, cv2.RANSAC, 5.0)

    return homography, status
