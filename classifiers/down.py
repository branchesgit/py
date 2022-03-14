import cv2
import os

root = "D:\\study\\py\\imgs\\numbers\\"
nine = "9\\"
six = "6\\"

if __name__ == "__main__":
    path = root + nine
    files = os.listdir(path)
    i = 0
    for file in files:
        print(path, file)
        img = cv2.imread(path + file, 0)
        img = cv2.flip(img, -1)
        cv2.imwrite(root + six + file, img)




