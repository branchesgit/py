import cv2
from matplotlib.cbook import ls_mapper
import numpy as np
from functools import cmp_to_key
from rect import Line

# 在Y轴上的投影
def Y_Project(binary):
    h, w = binary.shape

    # 水平投影
    hprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建h长度都为0的数组
    h_h = [0]*h
    for j in range(h):
        for i in range(w):
            if binary[j,i] == 0:
                h_h[j] += 1
    # 画出投影图
    for j in range(h):
        for i in range(h_h[j]):
            hprojection[j,i] = 255

    return h_h, hprojection

    
# 在X方向投影
def X_Project(binary):
    h, w = binary.shape
    # 垂直投影
    vprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建 w 长度都为0的数组
    w_w = [0]*w
    for i in range(w):
        for j in range(h):
            if binary[j, i ] == 0:
                w_w[i] += 1

    for i in range(w):
        for j in range(w_w[i]):
            vprojection[j,i] = 255
    
    cv2.imwrite('./imgs/row.png', vprojection)
    return w_w, vprojection


def closed_rectangle(mat, min_area):
    ret,thresh = cv2.threshold(mat,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    height, w = mat.shape
    for i in range(0,len(contours)):  
        x, y, w, h = cv2.boundingRect(contours[i])   
        
        if  h < 3 * height / 4:
            cv2.rectangle(mat, (x,y), (x+w,y+h), (0,0,0), -1) 

