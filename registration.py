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


def registrate(drone_img_ori, pcl_img_ori, args):
    common_args = {
        'use_mask': args.mask,
        'debug': args.debug
    }

    # Preprocess Images
    img_preprocessor = Preprocessor(drone_img_ori, pcl_img_ori)
    img_preprocessor.preprocessing()
    drone_img, pcl_img, masked_pcl_img, pcl_mask = img_preprocessor.get_processed_imgs()

    # Extract Features
    drone_feature_extractor = FeatureExtractor(drone_img, "SIFT")
    pcl_feature_extractor = FeatureExtractor(pcl_img, "SIFT")

    drone_feature_extractor.compute()

    if common_args['use_mask'] is True:
        pcl_feature_extractor.compute(mask=pcl_mask)

    else:
        pcl_feature_extractor.compute(mask=None)

    drone_features, drone_descs = drone_feature_extractor.get_features_and_descriptors()
    pcl_features, pcl_descs = pcl_feature_extractor.get_features_and_descriptors()

    # Find Matching
    matcher = Matcher(drone_features, drone_descs, pcl_features, pcl_descs)
    matcher.extract_match()
    good_matchs = matcher.get_good_matchs()

    # Find Homography
    homography, status = find_homography(
        drone_features, pcl_features, good_matchs)

    # Show matches
    #matcher.draw_matches(drone_img, pcl_img , status, homography)
    #matcher.draw_matches(drone_img, pcl_img , None, homography)
    #matcher.draw_matches(drone_img, pcl_img )

    registated_image = cv2.warpPerspective(
        drone_img_ori, homography, (pcl_img.shape[1], pcl_img.shape[0]))

    ret_image = cv2.add(registated_image, cv2.cvtColor(
        pcl_img, cv2.COLOR_GRAY2BGR))

    # plt.imshow(ret_image)
    # plt.show()

    return ret_image


def find_homography(features1, features2, matches):
    key_points1 = []
    key_points2 = []

    for match in matches:
        key_points1.append(features1[match.trainIdx])
        key_points2.append(features2[match.queryIdx])

    src_points = np.array([k.pt for k in key_points1])
    dst_points = np.array([k.pt for k in key_points2])

    homography, status = cv2.findHomography(
        src_points, dst_points, cv2.RANSAC, 5.0, maxIters=500000)

    return homography, status
