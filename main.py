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
    print('start')
    common_args = {
        'drone_folder_path': args.drone_folder_path,
        'pcl_path': args.pcl_path,
        'drone_mask_path':args.drone_mask_path,
    }

    image_list = glob.glob(os.path.join(
        common_args['drone_folder_path'], ('*.JPG')))

    pcl_img_loader = Loader()
    drone_img_loader = Loader()
    mask_img_loader = Loader()

    pcl_img_loader.load_img(os.path.join(common_args['pcl_path'], 'pcl.png'))

    resultWriter = ResultWriter(args)

    for idx, drone_path in enumerate(image_list):
        print(idx)
        mask_path = os.path.join(common_args['drone_mask_path'], drone_path.split("/")[-1].split(".")[0] + ".png")
        drone_img_loader.load_img(drone_path)
        mask_img_loader.load_img(mask_path)

        drone_image = drone_img_loader.get_img()
        pcl_image = pcl_img_loader.get_img()
        mask_image = mask_img_loader.get_img()

        result = registration.registrate(drone_image, pcl_image, mask_image, args)
        resultWriter.saveResults(result, idx)

if __name__ == '__main__':
    args = parser.make_parser()
    main(args)
