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


def registrate(drone_img_ori, pcl_img_ori, mask_image, args):
    common_args = {
        'pcl_mask': args.pcl_mask,
        'drone_mask': args.drone_mask,
        'save_masked_pcl': args.save_masked_pcl,
        'save_masked_drone': args.save_masked_drone,
        'save_keypoints': args.save_keypoints,
        'save_csv': args.save_csv,
        'save_matching': args.save_matching
    }

    result = {}

    # Preprocess Images
    img_preprocessor = Preprocessor(drone_img_ori, pcl_img_ori, mask_image)
    img_preprocessor.preprocessing()
    imgs = img_preprocessor.get_processed_imgs()

    processed_drone_img = imgs['processed_drone_img']
    processed_pcl_img = imgs['processed_pcl_img']
    processed_drone_mask = imgs['processed_drone_mask']
    processed_pcl_mask = imgs['processed_pcl_mask']
    masked_drone_img = imgs['masked_drone_img']
    masked_pcl_img = imgs['masked_pcl_img']

    if common_args['save_masked_pcl'] is True:
        result.update({'masked_pcl': masked_pcl_img})

    if common_args['save_masked_drone'] is True:
        result.update({'masked_drone': masked_drone_img})

    # Extract Features
    drone_feature_extractor = FeatureExtractor(
        processed_drone_img, "SIFT", args)
    pcl_feature_extractor = FeatureExtractor(processed_pcl_img, "SIFT", args)

    if common_args['pcl_mask'] is True:
        print("pcl_mask: True")
        pcl_feature_extractor.compute(mask=processed_pcl_mask)
    else:
        print("No pcl_mask")
        pcl_feature_extractor.compute(mask=None)

    if common_args['drone_mask'] is True:
        print("drone_mask: True")
        drone_feature_extractor.compute(mask=processed_drone_mask)
    else:
        print('No drone_mask')
        drone_feature_extractor.compute(mask=None)

    drone_features, drone_descs = drone_feature_extractor.get_features_and_descriptors()

    pcl_features, pcl_descs = pcl_feature_extractor.get_features_and_descriptors()

    if common_args['save_keypoints'] is True:
        keypoints_lidar = cv2.drawKeypoints(pcl_img_ori, pcl_features, outImage=np.array([]), color=(0, 0, 255),
                                            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        keypoints_drone = cv2.drawKeypoints(drone_img_ori, drone_features, outImage=np.array([]), color=(0, 0, 255),
                                            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        result.update({'keypoints_lidar_image': keypoints_lidar})
        result.update({'keypoints_drone_image': keypoints_drone})

    # Find Matching
    matcher = Matcher(drone_features, drone_descs, pcl_features, pcl_descs, args)
    matcher.extract_match()

    raw_matchs = matcher.get_matchs()
    good_matchs = matcher.get_good_matchs()

    # Find Homography
    homography, status = find_homography(
        drone_features, pcl_features, good_matchs, args)
 
    if common_args['save_csv'] is True:
        result.update({'drone_total_keypoints': len(drone_features)})
        result.update({'pcl_total_keypoints': len(pcl_features)})
        result.update({'num_inliers': (status.ravel().astype(int) == 1).sum()})
        result.update({'num_raw_matches': len(raw_matchs)})
        result.update({'num_good_matches': len(good_matchs)})
        result.update({'homography': homography})

    if common_args['save_matching'] is True:
        matching1 = matcher.draw_matches(
            processed_drone_img, processed_pcl_img, status, homography)
        matching2 = matcher.draw_matches(
            processed_drone_img, processed_pcl_img, None, homography)
        matching3 = matcher.draw_matches(
            processed_drone_img, processed_pcl_img)
        result.update({'matching1': matching1})
        result.update({'matching2': matching2})
        result.update({'matching3': matching3})

    registated_image = cv2.warpPerspective(
        drone_img_ori, homography, (processed_pcl_img.shape[1], processed_pcl_img.shape[0]))

    ret_image = cv2.add(registated_image, cv2.cvtColor(
        processed_pcl_img, cv2.COLOR_GRAY2BGR))

    result.update({'image': ret_image})
    return result


def find_homography(features1, features2, matches, args):
    common_args = {
        'ransac_maxIters': args.ransac_maxIters,
        'ransac_confidence': args.ransac_confidence
    }

    key_points1 = []
    key_points2 = []

    for match in matches:
        key_points1.append(features1[match.trainIdx])
        key_points2.append(features2[match.queryIdx])

    src_points = np.array([k.pt for k in key_points1])
    dst_points = np.array([k.pt for k in key_points2])

    homography, status = cv2.findHomography(
        src_points, dst_points, cv2.RANSAC, confidence=common_args['ransac_confidence'], maxIters=common_args['ransac_maxIters'])

    return homography, status
