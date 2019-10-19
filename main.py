import os
import glob
import parser
import cv2
import registration
from imageLoader import ImageLoader as Loader
import numpy as np
from utils import ResultWriter

np.random.seed(42)  # Reproducibility


def main(args):
    common_args = {
        'drone_folder_path': args.drone_folder_path,
        'pcl_path': args.pcl_path,
    }

    image_list = glob.glob(os.path.join(
        common_args['drone_folder_path'], ('*.JPG')))

    pcl_img_loader = Loader()
    drone_img_loader = Loader()

    pcl_img_loader.load_img(common_args['pcl_path'])

    resultWriter = ResultWriter(args)

    for idx, drone_path in enumerate(image_list):
        drone_img_loader.load_img(drone_path)

        drone_image = drone_img_loader.get_img()
        pcl_image = pcl_img_loader.get_img()

        result = registration.registrate(drone_image, pcl_image, args)
        resultWriter.saveResults(result, idx)


if __name__ == '__main__':
    args = parser.make_parser()
    main(args)
