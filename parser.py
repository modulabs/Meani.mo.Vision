import argparse


def make_parser():
    parser = argparse.ArgumentParser(description='Meani.mo Vision')
    parser.add_argument(
        '--drone_path',
        "-d",
        default='./images/drone1.bmp',
        required=False,
        help='Path in which drone image is located')
    parser.add_argument(
        '--lidar_path',
        "-l",
        default='./images/lidar1.bmp',
        required=False,
        help='Path in which lidar image is located')
    parser.add_argument(
        '--dst_path',
        "-o",
        default='./output.bmp',
        required=False,
        help='Path in which result is saved')

    return parser.parse_args()
