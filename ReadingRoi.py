from read_roi import read_roi_zip
import cv2
import numpy as np
from matplotlib.path import Path


#img = cv2.imread('j.png',0)
#kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(img,kernel,iterations = 1)

def show_each_border(img):
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img_list = ['3895_01.tif', '3895_02.tif', '3895_03.tif', '3895_04.tif']
roi_list =  ['3895_01.zip', '3895_02.zip', '3895_03.zip', '3895_04.zip']
kernel_one = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
kernel_two = np.ones((3,3),np.uint8)
img = cv2.imread(img_list[0])
rois = read_roi_zip(roi_list[0])
height_o, width_o, channel = img.shape
finished_image = np.zeros((height_o, width_o), np.uint8)
h = height_o
w = width_o

rois_len = len(rois)
for iter, roi in enumerate(rois):
    """
    width = max(rois[roi]['x']) - min(rois[roi]['x'])
    height = max(rois[roi]['y']) - min(rois[roi]['y'])

    new_img = np.zeros((height_o, width_o),np.uint8)
    for i in range(len(rois[roi]['x'])):
       new_img[rois[roi]['y'][i], rois[roi]['x'][i]] = 255
    test = True
    for x in range(min(rois[roi]['y']) , max(rois[roi]['y']) + 1):
        test = True
        first = False
        last = False
        for y in range(min(rois[roi]['x']), max(rois[roi]['x']) + 1):
            if new_img[x, y] == 255 and test is True:
                first = y
                test = False
            if new_img[x, y] == 255:
                last = y
        if first and last:
            for y_slice in range(first,last):
                new_img[x, y_slice] = 255
    """
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
    mask = 255 * mask
    mask = np.array(mask, dtype='uint8')
    # EROSION
    eroded_image = cv2.erode(mask, kernel_one, iterations = 1)
    eroded_image = cv2.erode(eroded_image, kernel_two, iterations=1)
    border_erosion = mask - eroded_image
    # DILATION
    dilation = cv2.dilate(mask, kernel_two, iterations=1)
    border_dilatation = dilation - mask
    end_result = cv2.add(border_erosion, border_dilatation)

    """
    middle_x = (max(rois[roi]['x'])+min(rois[roi]['x']))/2
    middle_y = (max(rois[roi]['y'])+min(rois[roi]['y']))/2
    end_result[int(middle_y), int(middle_x)] = 255
    """
    finished_image = cv2.add(finished_image, end_result)
    print(f'{int(iter/rois_len*100)}%', end="")






cv2.imwrite("test2.tif", finished_image)
show_each_border(finished_image)