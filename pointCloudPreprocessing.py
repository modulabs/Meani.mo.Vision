import cv2
import numpy as np

def pcl_image_preprocessing2(img):

    img2 = cv2.medianBlur(img, 5)
    img2[img2 == 224] = 0
    ret, mask = cv2.threshold(img2, 1, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    mask_ero = cv2.erode(mask, kernel, iterations = 7)
    contours = cv2.findContours(mask_ero, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    max_idx = 0
    max_len = 0
    for i in range(len(contours[1])):
        c = contours[1][i]
        if(max_len < len(c)):
            max_len = len(c)
            max_idx = i
            
    selected_contour = contours[1][max_idx].reshape(1, -1, 2)

    mask2 = np.zeros(mask_ero.shape, np.uint8)
    mask2 = cv2.fillPoly(mask2, selected_contour, color=[255])

    mask3 = cv2.dilate(mask2, kernel, iterations = 5)
    img_croped = cv2.bitwise_and(img2, mask3, None)

    return img_croped, mask3

# python ./pointCloudPreprocessing.py "C:\\Data\\[YounSae] point data\\Sample Data (2)\\CASE 4\\case4(raw).png"
if __name__ == '__main__':
    import sys
    import os

    if (len(sys.argv) < 2):
        print('Ex: batch <DESTNATION FILE>')
        exit(1)

    dst_image_fname = sys.argv[1]
    dst_name = os.path.basename(dst_image_fname)
    dst_img = cv2.imread(dst_image_fname, cv2.IMREAD_GRAYSCALE)

    dst_cropped, dst_mask = pcl_image_preprocessing2(dst_img)
    cv2.imwrite('batch_cropped.png', dst_cropped)
