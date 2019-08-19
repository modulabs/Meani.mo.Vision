import math
import os
import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg
from imageLoader import ImageLoader as Loader
from preprocessor import Preprocessor
from featureDetector import FeatureDetector
from matcher import Matcher

def registration(drone_img_path,lidar_img_path, outout_file):


    img_loader = Loader(drone_img_path,lidar_img_path)
    img_loader.load_imgs()
    drone_raws, lidar_raws = img_loader.get_imgs()



    img_preprocessor = Preprocessor(drone_raws,lidar_raws)
    img_preprocessor.preprocessing()
    drone_img,lidar_img = img_preprocessor.get_processed_imgs()



    feature_detector = FeatureDetector(drone_img,"SIFT",lidar_img,"SIFT")
    feature_detector.compute_features_and_descriptor()
    drone_features, drone_descs = feature_detector.get_feature_and_descriptor(img_type="drone")
    lidar_features, lidar_descs = feature_detector.get_feature_and_descriptor(img_type="lidar")



    matcher = Matcher(drone_features,drone_descs,lidar_features,lidar_descs)
    matcher.extract_match()
    matcher.find_homography()
    matcher.draw_matches(drone_img,lidar_img,outout_file)

    return



if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print >> sys.stderr, ("Usage: %s <image_dir> <key_frame> <output>" % sys.argv[0])
        sys.exit(-1)

    registration(sys.argv[1], sys.argv[2], sys.argv[3])