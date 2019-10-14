import argparse


def make_parser():
    parser = argparse.ArgumentParser(description='Meani.mo Vision')
    parser.add_argument(
        '--drone_folder_path',
        '-s',
        default='/Volumes/ZetDrive64/Sample_Data_2/CASE 5',
        required=False,
        help='Path in which drone image folder is located')
    parser.add_argument(
        '--pcl_path',
        '-l',
        default='/Volumes/ZetDrive64/Sample_Data_2/CASE 5/case5(raw).png',
        required=False,
        help='Path in which lidar image is located')
    parser.add_argument(
        '--dst_path',
        '-o',
        default='./output.bmp',
        required=False,
        help='Path in which result is saved')
    parser.add_argument(
        '--experiment_num',
        '-e',
        default=0,
        help='Experiment Number')
    parser.add_argument(
        '--debug',
        '-d',
        default=True,
        help='Imshow Intermediate Results'
    )
    parser.add_argument(
        '--mask',
        '-m',
        default=False,
        help='Applying binary mask to a pcl image'
    )
    parser.add_argument(
        '--record',
        default=True,
        help='Record result video for making GIF'
    )

    return parser.parse_args()
