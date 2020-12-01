from read_roi import read_roi_zip
import cv2
import numpy as np
from matplotlib.path import Path
from os import listdir
from os.path import isfile, join
import time
import datetime


def show_each_border(img):
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


start_time = datetime.datetime.now()
path = './Rawdata/Train/'
img_list  = [path + img for img in listdir(path) if ".tif" in img and isfile(join(path, img))]
kernel_one = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
kernel_two = np.ones((3,3),np.uint8)
for img_num, img_path in enumerate(img_list):
    try:
        img = cv2.imread(img_path)
        rois = read_roi_zip(img_path.replace(".tif", ".zip"))
        height_o, width_o, channel = img.shape
        finished_image = np.zeros((height_o, width_o), np.uint8)
        h = height_o
        w = width_o
        rois_len = len(rois)
        for iter, roi in enumerate(rois):
            x = rois[roi]['x']
            y = rois[roi]['y']
            n = len(x)
            i = 0
            ListOfCorners = []
            for i in range(i, n):
                ListOfCorners.append((int((y[i])), int((x[i]))))
            poly_path = Path(ListOfCorners)
            Nx, Ny = np.mgrid[:h, :w]
            coordinates = np.hstack((Nx.reshape(-1, 1), Ny.reshape(-1, 1)))
            mask = poly_path.contains_points(coordinates)
            mask = mask.reshape(h, w)
            mask = np.array(mask, dtype=bool)
            mask = np.array(mask, dtype='uint8')
            # EROSION
            eroded_image = cv2.erode(mask, kernel_one, iterations = 1)
            eroded_image = cv2.erode(eroded_image, kernel_two, iterations=1)
            border_erosion = mask - eroded_image
            # DILATION
            dilation = cv2.dilate(mask, kernel_two, iterations=1)
            border_dilatation = dilation - mask
            end_result = cv2.add(border_erosion, border_dilatation)

            eroded_image[eroded_image == 1] = 2
            end_result = cv2.add(end_result, eroded_image)
            imageMask = (end_result != 0)
            finished_image[imageMask] = end_result[imageMask]


            print(f'\r{int(iter/rois_len*100)}%  -  {img_num+1}/{len(img_list)}   ', datetime.datetime.now() - start_time , end="") ## shows progress


        cv2.imwrite(img_path.replace(".tif", "_mask.tif"), finished_image)

    except Exception as e:
        print(e)
        pass
