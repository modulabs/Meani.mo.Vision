import os
import glob
import parser
import cv2
import registration
from imageLoader import ImageLoader as Loader
import numpy as np

np.random.seed(42)  # Reproducibility


def makedirs(path):
    # Intended behavior: try to create the directory,
    # pass if the directory exists already, fails otherwise.
    # Meant for Python 2.7/3.n compatibility.
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def main(args):
    common_args = {
        'experiment_num': args.experiment_num,
        'drone_folder_path': args.drone_folder_path,
        'pcl_path': args.pcl_path,
        'debug': args.debug
    }

    dataSetStr = os.path.basename(
        os.path.normpath(common_args['drone_folder_path']))
    dst_path = os.path.join(
        './', 'experiment' + str(common_args['experiment_num']) + '_' + dataSetStr)
    makedirs(dst_path)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    video_dst = os.path.join(dst_path, 'output.avi')
    vid = cv2.VideoWriter(video_dst, fourcc, 1, (512, 512), True, )

    image_list = glob.glob(os.path.join(
        common_args['drone_folder_path'], ('*.JPG')))
    pcl_path = common_args['pcl_path']

    pcl_img_loader = Loader()
    drone_img_loader = Loader()

    pcl_img_loader.load_img(pcl_path)

    for idx, drone_path in enumerate(image_list):
        drone_img_loader.load_img(drone_path)

        drone_image = drone_img_loader.get_img()
        pcl_image = pcl_img_loader.get_img()

        result = registration.registrate(
            drone_image, pcl_image, args, dst_path, idx, debug=common_args['debug'])
        cv2.imwrite(os.path.join(
            dst_path, 'result_' + str(idx) + '.jpg'), result)

        vid.write(cv2.resize(result, (512, 512)))

    vid.release()


if __name__ == '__main__':
    args = parser.make_parser()
    main(args)
