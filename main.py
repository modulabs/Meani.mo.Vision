import parser
import cv2
import registration
from imageLoader import ImageLoader as Loader
import numpy as np

np.random.seed(42)  # Reproducibility


def main(args):
    drone_img_loader = Loader()
    lidar_img_loader = Loader()

    drone_img_loader.load_img(args.drone_path)
    lidar_img_loader.load_img(args.lidar_path)

    drone_image = drone_img_loader.get_img()
    lidar_image = lidar_img_loader.get_img()

    result = registration.registrate(drone_image, lidar_image)

    cv2.imwrite(args.dst_path, result)


if __name__ == '__main__':
    args = parser.make_parser()
    main(args)
