
from fileinput import close
from math import ceil
from project import vProject
import cv2
from rect import Rect, sort_y, sort_x
import numpy as np
class OptionClassifier():
    def set_direction(self, direction):
        self.direction = direction

    def classifier(self, mat):
        kernel = np.ones((5,5),np.uint8)
        cv2.morphologyEx(mat,cv2.MORPH_OPEN,kernel)
        ret,thresh = cv2.threshold(mat,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        areas = []
        height, width = mat.shape
        m = 1000
        for i in range(0,len(contours)):  
            x, y, w, h = cv2.boundingRect(contours[i])   
            areas.append(w * h)
            m = min(m, w * h)
            if w < 3 * width / 4 and h < 3 * height / 4:
                if w * h >= 10:
                    cv2.rectangle(mat, (x,y), (x+w,y+h), (0,0,0), -1) 

        # 对v_project进行逻辑处理.
        w_w, v_project = vProject(mat)
        contours, hierarchy = cv2.findContours(v_project,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        x_rects = []
        
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            rect = Rect(x, y, w, h)
            x_rects.append(rect)
            
        ws = []   
        gaps = []
        x_rects.sort(key=sort_x)
        for i in range(len(x_rects)):
            rect = x_rects[i]
            ws.append(rect.w)
            if i >= 1:
                gaps.append(rect.x - x_rects[i -1].x - x_rects[i-1].w)

        c_gaps = [i for i in gaps]
        gaps.sort()
        gaps_len = len(gaps) - 1
        m = gaps[gaps_len]
        count = 0
        middle = gaps[int(gaps_len / 2)] + 1
        kernel = np.ones((middle, middle), np.uint8)
        v_project = cv2.dilate(v_project,kernel)

        cv2.imwrite("./imgs/vpro.png", v_project)

        # value = ceil((middle + m) / 2)
        # while gaps_len >= 0:
        #     gaps_len -= 1
        #     if gaps[gaps_len] >= value:
        #         count += 1
        
        # n = gaps[gaps_len - count + 1]
        
        # indexs = []
        # for i in range(len(c_gaps)):
        #     if c_gaps[i] >= n and c_gaps[i] <= m:
        #         indexs.append(i)
        # print(indexs, c_gaps)
        

    # 得到最小的矩形框
    def get_min_rect(self, mat, rect):
        print('get_min_rect')
