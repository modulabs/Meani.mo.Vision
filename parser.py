import argparse


def make_parser():
    parser = argparse.ArgumentParser(description='Meani.mo Vision')

    # path arguments
    parser.add_argument('--drone_folder_path', '-s',
                        default='/media/visionnoob/dataset/Sample Data (2)/ex1/CASE1_1',
                        required=False, help='Path in which drone image folder is located')

    parser.add_argument('--pcl_path', '-l',
                        default='/media/visionnoob/dataset/Sample Data (2)/ex1/CASE1_1/case1(raw).png',
                        required=False, help='Path in which lidar image is located')

    parser.add_argument('--experiment_num', '-e',
                        default=11, help='Experiment Number')

    # Algorithm parameter arguments
    parser.add_argument('--find_good_match', default=True, help='')
    parser.add_argument('--remove_duplicated', default=True, help='')

    # Binary Mask
    parser.add_argument('--pcl_mask', default=True,
                        help='Applying binary mask to a pcl image')
    parser.add_argument('--drone_mask', default=False,
                        help='Applying binary mask to a drone image')

    # RANSAC (see https://docs.opencv.org/3.4.0/d9/d0c/group__calib3d.html#ga4abc2ece9fab9398f2e560d53c8c9780)
    parser.add_argument('--ransac_maxIters', default=2000, type=int,
                        help='The maximum number of RANSAC iterations, 2000 is the maximum it can be.')
    parser.add_argument('--ransac_confidence', default=0.995, type=float,
                        help='Confidence level, between 0 and 1 (default:0.995).')

    # SIFT
    parser.add_argument('--SIFT_nfeatures', default=0, type=float,
                        help='The number of best features to retain. The features are ranked by their scores (default:0)')
    parser.add_argument('--SIFT_nOctaveLayers', default=3, type=float,
                        help='The number of layers in each octave. 3 is the value used in D (default=3).')
    parser.add_argument('--SIFT_contrastThreshold', default=0.04, type=float,
                        help='The contrast threshold used to filter out weak features in semi-uniform (low-contrast) regions. \
                              The larger the threshold, the less features are produced by the detector(default=0.04).')
    parser.add_argument('--SIFT_edgeThreshold', default=50, type=float,
                        help='The threshold used to filter out edge-like features. Note that the its meaning is different from the contrastThreshold, i.e. the larger the edgeThreshold, the less features are filtered out (more features are retained), (default: 10).')
    parser.add_argument('--SIFT_sigma', default=1.6, type=float,
                        help='The sigma of the Gaussian applied to the input image at the octave #0. If your image is captured with a weak camera with soft lenses, you might want to reduce the number.')

    # Debug & imshow & writing arguments
    parser.add_argument('--debug', default=True,
                        help='Imshow Intermediate Results')
    parser.add_argument('--save_video', default=True,
                        help='Record result video for making GIF')
    parser.add_argument('--save_csv', default=True, help='Save csv')
    parser.add_argument('--save_masked_pcl', default=True,
                        help='Save masked pcl image')
    parser.add_argument('--save_masked_drone', default=True,
                        help='Save masked drone image')
    parser.add_argument('--save_matching', default=True,
                        help='Save matching images')
    parser.add_argument('--save_keypoints', default=True,
                        help='Save keypoints images')

    return parser.parse_args()
