import cv2
import numpy as np
from os import listdir
from os.path import isfile, join




def show_image(img):
    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


path = './Rawdata/Train/'

img_path_list  = [path + img for img in listdir(path) if ".tif" in img and "mask" not in img and isfile(join(path, img))]


for iteration, img_path in enumerate(img_path_list):
    try:
        img = cv2.imread(img_path, 0)
        imgMask = cv2.imread(img_path.replace(".tif", "_mask.tif"))
        img_rgb = cv2.imread(img_path)
        ret, imgT = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        imgT = 255 - imgT
        x_max, y_max = imgT.shape
        x_parts = [x_pos for x_pos in range(0, x_max, 256) if x_pos + 512 < x_max]
        y_parts = [y_pos for y_pos in range(0, y_max, 256) if y_pos + 512 < y_max]
        if x_max - 512 not in x_parts:
            x_parts.append(x_max - 512)
        if y_max - 512 not in y_parts:
            y_parts.append(y_max - 512)

        for x in x_parts:
            for y in y_parts:
                img_slice = imgT[x:x+512, y:y+512]
                if len(img_slice[img_slice > 0]) / len(img_slice[img_slice >= 0]) >= 0.2:

                    cv2.imwrite(img_path.replace(".tif", f"_{x}_{y}.tif"), img_rgb[x:x+512, y:y+512])
                    cv2.imwrite(img_path.replace(".tif", f"_{x}_{y}_mask.tif"), imgMask[x:x+512, y:y+512])
        print(f'\r{iteration}/{len(img_path_list)}',  end="")  










    except Exception as e:
        print("Error", e)
        pass