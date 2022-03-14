import cv2
import os
import numpy as np
import math
from util.projection import Y_Project, X_Project

root = "D:\\study\\py\\imgs\\numbers\\"
number = "1\\"
test = "test\\"
length = 28

if __name__ == '__main__':
    numer = test
    path = root + number
    files = os.listdir(path)

    for file in files:
        gray = cv2.imread(path + file, 0)

        gray = cv2.resize(gray, (28, 28))
        (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        while np.sum(gray[0]) == 0:
            gray = gray[1:]
        while np.sum(gray[:, 0]) == 0:
            gray = np.delete(gray, 0, 1)
        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]
        while np.sum(gray[:, -1]) == 0:
            gray = np.delete(gray, -1, 1)
        rows, cols = gray.shape

        if rows > cols:
            factor = 20.0 / rows
            rows = 20
            cols = int(round(cols * factor))
            gray = cv2.resize(gray, (cols, rows))
        else:
            factor = 20.0 / cols
            cols = 20
            rows = int(round(rows * factor))
            gray = cv2.resize(gray, (cols, rows))

        # 补边
        cols_padding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
        rows_padding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
        gray = np.lib.pad(gray, (rows_padding, cols_padding), 'constant')
        cv2.imwrite(root + "c_" + number + file + "_c.png", gray)
