from read_roi import read_roi_zip
import cv2
import numpy as np

#img = cv2.imread('j.png',0)
#kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(img,kernel,iterations = 1)


img_list = ['3895_01.tif', '3895_02.tif', '3895_03.tif', '3895_04.tif']
roi_list =  ['3895_01.zip', '3895_02.zip', '3895_03.zip', '3895_04.zip']
kernel_one = np.array([[0,1,0],[1,1,1],[0,1,0]])
kernel_two = np.ones((5,5),np.uint8)
img = cv2.imread(img_list[3])
rois = read_roi_zip(roi_list[3])
heght_o, width_o, channel = img.shape
#erosion = cv2.erode(img,kernel,iterations = 1)
#dilation = cv2.dilate(img,kernel,iterations = 1)

for roi in rois:
   # width = max(rois[roi]['x']) - min(rois[roi]['x'])
    #height = max(rois[roi]['y']) - min(rois[roi]['y'])
    width = max(rois[roi]['x']) + 5
    height = max(rois[roi]['y']) + 5
    new_img = np.ones((heght_o, width_o,1),np.uint8)*255
    for i in range(len(rois[roi]['x'])):
       # new_img[rois[roi]['y'][i] - max(rois[roi]['y']),rois[roi]['x'][i] - max(rois[roi]['x'])] = 0
       new_img[rois[roi]['y'][i], rois[roi]['x'][i]] = 0
    test = True
    for x in range(height):
        test = True
        first = False
        last = False
        for y in range(width):
            if new_img[x, y] == 0 and test is True:
                first = y
                test = False
            if new_img[x, y] == 0:
                last = y
        if first and last:
            for y_slice in range(first,last):
                new_img[x, y_slice] = 0





    cv2.imshow("lol", new_img)
    cv2.imwrite("test.tif",new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  #  test = img[rois[roi]['y'], rois[roi]['x']]



print("finished")
cv2.imwrite("test.tif",new_img)
#cv2.imshow("lol",img)
#test = img[min(rois[roi]['y']):max(rois[roi]['y']), min(rois[roi]['x']):max(rois[roi]['x'])]
#print(roi)
#test = img[rois[roi]['y'], rois[roi]['x']]
#cv2.imshow("lol",new_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()