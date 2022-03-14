import cv2
import os
import numpy as np
from util.projection import Y_Project, X_Project
from util.data import get_lines, get_max_value, filter_zero
from rect import get_gaps

path = "D:\\study\\py\\imgs\\sn\\19\\"
number = "19"
root = "D:\\study\\py\\imgs\\sn\\"


if __name__ == "__main__":
    files = os.listdir(path)

    for file in files:
        if not os.path.isdir(path + file):
            print('print====', path + file)
            img = cv2.imread(path + file, 0)
            h_h, y_projection = Y_Project(img)
            height, width = img.shape
            c_h_h = filter_zero(h_h)
            max_value = get_max_value(c_h_h)
            lines = get_lines(h_h, 1, max_value, width * 3, False)
            cv2.imwrite(path + "t\\" + file, y_projection)

            if len(lines) == 1:
                line = lines[0]
                img = img[max(0, line.start - 2): min(height, line.start + line.h + 4), 0: width]
                w_w, x_projection = X_Project(img)
                c_w_w = filter_zero(w_w)
                max_value = get_max_value(c_w_w)
                lines = get_lines(w_w, 1, max_value, height, False)
                cv2.imwrite(path + "t\\" + file, x_projection)
                height, width = img.shape
                if len(lines) == 2:
                    i = 0
                    for line in lines:
                        if i == 0:
                            cv2.imwrite(root + number[0:1] + "\\" + file, img[0: height, line.start - 2: line.start + line.h + 4])
                        else:
                            cv2.imwrite(root + number[1:2] + "\\" + file, img[0: height, line.start - 2: line.start + line.h + 4])
                        i += 1

            else:
                print("lines's length is " , len(lines))