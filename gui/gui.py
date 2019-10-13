import os
import sys
import cv2
import numpy as np

DRONE_IMAGE_SIZE = (5300, 7950)

CASE1_CONFIG = ["./images/CASE_1", "drone7.JPG", 800, 600, 4096, 4096]
CASE2_CONFIG = ["./images/CASE_2", "drone10.JPG", 409, 1200, 4096, 4096]
CASE3_CONFIG = ["./images/CASE_3", "drone8.JPG", 700, 200, 4096, 4096]
CASE4_CONFIG = ["./images/CASE_4", "drone1.JPG", 300, 700, 4096, 4096]
CONFIG = CASE2_CONFIG

# set lidar roi and make size (4096 x 4096)
lidar_roi_y = CONFIG[2]
lidar_roi_x = CONFIG[3]
lidar_roi_height = CONFIG[4]
lidar_roi_width = CONFIG[4]

lidar_roi_center_x = lidar_roi_width / 2
lidar_roi_center_y = lidar_roi_height / 2
lidar_roi_center_x = int(lidar_roi_center_x)
lidar_roi_center_y = int(lidar_roi_center_y)
lidar_roi_width_height = 600

drone_image_height = 5300
drone_image_width = 7950

drone_roi_center_x = drone_image_width / 2
drone_roi_center_y = drone_image_height / 2
drone_roi_center_x = int(drone_roi_center_x)
drone_roi_center_y = int(drone_roi_center_y)
drone_roi_width_height = 600

lidar_pos_change = True
drone_pos_change = True

# mouse callback function


def lidar_move(event, x, y, flags, param):
    global lidar_roi_center_x
    global lidar_roi_center_y
    global lidar_pos_change
    if event == cv2.EVENT_LBUTTONDOWN:
        lidar_roi_center_x = x * 1 / param
        lidar_roi_center_x = int(lidar_roi_center_x)
        lidar_roi_center_y = y * 1 / param
        lidar_roi_center_y = int(lidar_roi_center_y)
        lidar_pos_change = True

# mouse callback function


def drone_move(event, x, y, flags, param):
    global drone_roi_center_x
    global drone_roi_center_y
    global drone_pos_change
    if event == cv2.EVENT_LBUTTONDOWN:
        drone_roi_center_x = x * 1 / param
        drone_roi_center_x = int(drone_roi_center_x)
        drone_roi_center_y = y * 1 / param
        drone_roi_center_y = int(drone_roi_center_y)
        drone_pos_change = True


def main():
    global lidar_pos_change
    global drone_pos_change
    global drone_roi_width_height
    lidar_imshow_scale = 0.1
    drone_imshow_scale = 0.08
    cv2.namedWindow('lidar_image')
    cv2.namedWindow('drone_image')
    cv2.setMouseCallback('lidar_image', lidar_move, param=lidar_imshow_scale)
    cv2.setMouseCallback('drone_image', drone_move, param=drone_imshow_scale)

    DRONE_IMG_PATH = os.path.join(CONFIG[0], "drone", CONFIG[1])
    LIDAR_IMG_PATH = os.path.join(CONFIG[0], "lidar", "lidar.jpg")

    drone_image = cv2.imread(DRONE_IMG_PATH)
    lidar_image = cv2.imread(LIDAR_IMG_PATH)

    lidar_image = lidar_image[lidar_roi_y:lidar_roi_y +
                              lidar_roi_height, lidar_roi_x:lidar_roi_x + lidar_roi_width, :]
    drone_image = drone_image[0:drone_image_height, 0:drone_image_width, :]

    #resized_lidar = cv2.resize(lidar_image, dsize=None,fx=0.1, fy=0.1)
    #resized_drone = cv2.resize(drone_image, dsize=None,fx=0.1, fy=0.1)

    resized_lidar = cv2.resize(
        lidar_image, dsize=None, fx=lidar_imshow_scale, fy=lidar_imshow_scale)
    resized_drone = cv2.resize(
        drone_image, dsize=None, fx=drone_imshow_scale, fy=drone_imshow_scale)

    while(1):
        temp_lidar_image = resized_lidar.copy()
        temp_drone_image = resized_drone.copy()

        lidar_x1 = (lidar_roi_center_x - lidar_roi_width_height)
        scaled_lidar_x1 = int(lidar_x1 * lidar_imshow_scale)
        lidar_y1 = (lidar_roi_center_y - lidar_roi_width_height)
        scaled_lidar_y1 = int(lidar_y1 * lidar_imshow_scale)
        lidar_x2 = (lidar_roi_center_x + lidar_roi_width_height)
        scaled_lidar_x2 = int(lidar_x2 * lidar_imshow_scale)
        lidar_y2 = (lidar_roi_center_y + lidar_roi_width_height)
        scaled_lidar_y2 = int(lidar_y2 * lidar_imshow_scale)
        cv2.rectangle(temp_lidar_image,
                      (scaled_lidar_x1, scaled_lidar_y1),
                      (scaled_lidar_x2, scaled_lidar_y2),
                      (0, 0, 255), 2)

        drone_x1 = (drone_roi_center_x - drone_roi_width_height)
        scaled_drone_x1 = int(drone_x1 * drone_imshow_scale)
        drone_y1 = (drone_roi_center_y - drone_roi_width_height)
        scaled_drone_y1 = int(drone_y1 * drone_imshow_scale)
        drone_x2 = (drone_roi_center_x + drone_roi_width_height)
        scaled_drone_x2 = int(drone_x2 * drone_imshow_scale)
        drone_y2 = (drone_roi_center_y + drone_roi_width_height)
        scaled_drone_y2 = int(drone_y2 * drone_imshow_scale)

        cv2.rectangle(temp_drone_image,
                      (scaled_drone_x1, scaled_drone_y1),
                      (scaled_drone_x2, scaled_drone_y2),
                      (0, 0, 255), 2)

        if lidar_pos_change == True:
            lidar_roi_image = lidar_image[lidar_y1:lidar_y1 +
                                          lidar_roi_width_height*2, lidar_x1:lidar_x1+lidar_roi_width_height*2:]
            print(lidar_roi_width_height)
            lidar_pos_change = False

        if drone_pos_change == True:
            drone_roi_image = drone_image[drone_y1:drone_y1 +
                                          drone_roi_width_height*2, drone_x1:drone_x1+drone_roi_width_height*2:]
            drone_pos_change = False

        cv2.imshow('lidar_roi_image', cv2.resize(
            lidar_roi_image, dsize=(250, 250)))
        cv2.imshow('drone_roi_image', cv2.resize(
            drone_roi_image, dsize=(250, 250)))

        cv2.imshow('lidar_image', temp_lidar_image)
        cv2.imshow('drone_image', temp_drone_image)
        k = cv2.waitKey(40)
        if k == ord('o'):  # 's' key
            drone_roi_width_height += 10
        elif k == ord('p'):  # 's' key
            drone_roi_width_height -= 10
        elif k == ord('s'):
            save_lidar_image = cv2.resize(lidar_roi_image, dsize=(1200, 1200))
            save_drone_image = cv2.resize(drone_roi_image, dsize=(1200, 1200))
            cv2.imwrite("lidar.bmp", save_lidar_image)
            cv2.imwrite("drone.bmp", save_drone_image)

    # cv2.imshow('resized_drone',resized_drone)
    # cv2.waitKey()

#img = np.zeros((512,512,3), np.uint8)


# def main():
    # Create a black image, a window and bind the function to window

#    cv2.namedWindow('image')
#    cv2.setMouseCallback('image',draw_circle)

#    while(1):
#        cv2.imshow('image',img)
#        if cv2.waitKey(20) & 0xFF == 27:
#            break
#    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
