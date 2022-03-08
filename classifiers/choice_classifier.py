from re import S
from tracemalloc import start
import cv2
from classifier import Classifier
from option_classifier import OptionClassifier
from project import hProject, vProject, concentrated, get_target_concentrated
import numpy as np
from rect import Rect, sort_x, sort_y
class Line:
    def __init__(self, start, h):
        self.start = start
        self.length = h
        self.gap = 0



# 选择题切割.
class ChoiceClassifier(Classifier):
    pass
    
    def classifier(self):
        x, y, width, height = self.rect
        part = self.mat[y:y + height, x: x + width]
        c_choice_mat = self.mat[y:y + height, x: x + width].copy()
        
        ret,thresh = cv2.threshold(part,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        areas = []
        m = 1000
        for i in range(0,len(contours)):  
            x, y, w, h = cv2.boundingRect(contours[i])   
            areas.append(w * h)
            m = min(m, w * h)
            if w < 3 * width / 4 and h < 3 * height / 4:
                if w * h >= 10:
                    cv2.rectangle(part, (x,y), (x+w,y+h), (0,0,0), -1) 
        
        self.convengence(part, c_choice_mat)

    # 收缩范围，收敛处理
    def convengence(self, part, c_choice_mat):
        # y轴投影，
        h_h, hprojection = hProject(part)
        kernel = np.ones((5,5),np.uint8)
        cv2.morphologyEx(hprojection,cv2.MORPH_OPEN,kernel)
        contours, hierarchy = cv2.findContours(hprojection,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        y_rects = []
        hs = []
        for i in range(0, len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w * h >= 200:
                rect = Rect(x, y, w, h)
                y_rects.append(rect)
                hs.append(h)

        y_rects.sort(key=sort_y)
        hs.sort()
       # print(hs, y_rects)
        r = y_rects[0]
        er = y_rects[len(y_rects) - 1]
        # x, y, w, h = 
        rt = Rect(0, r.y, 0, er.y + er.h - r.y)
        cv2.imwrite("./imgs/hpro.png", hprojection)

        w_w, vprojection = vProject(part)
        cv2.morphologyEx(vprojection,cv2.MORPH_OPEN,kernel)
        cv2.imwrite("./imgs/vpro.png", vprojection)
        x_rects = []
        ws = []
        contours, hierarchy = cv2.findContours(vprojection,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            if w * h >= 200:
                rect = Rect(x, y, w, h)
                x_rects.append(rect)
                ws.append(w)
        x_rects.sort(key=sort_x)
        ws.sort()
        rt.x = x_rects[0].x
        rt.w = x_rects[len(x_rects) - 1].x + x_rects[len(x_rects) - 1].w - x_rects[0].x

        direction = "horition"
        if hs[0] < ws[0]:
            direction = "vertica"
        
        part = c_choice_mat[rt.y:rt.y + rt.h, rt.x: x + rt.w]
        cv2.imwrite("./imgs/c.png",part)
        optionClassifier = OptionClassifier()
        optionClassifier.set_direction(direction)
        optionClassifier.classifier(part)


    # 缩减范围，收敛处理
    #def convengence(self,part):
    #    h_h = hProject(part)
    #    c_h_h = [i for i in h_h]
    #    h_h.sort()
    #    # 取集中分布
    #    #for i in range(h_h):
    #    values = concentrated(h_h, 2)
    #    horizal_lines = self.draw_lines(values, c_h_h, part)
    #    hl = []
    #    for i in range(len(horizal_lines)):
    #        hl.append(horizal_lines[i].length)
    #        if i >= 1:
    #            horizal_lines[i - 1].gap = horizal_lines[i].start - horizal_lines[i-1].start - horizal_lines[i-1].length
    #
    #    hl = concentrated(hl, 1)
    #
    #    w_w = vProject(part)
    #    c_w_w = [i for i in w_w]
    #    w_w.sort()
    #    values = concentrated(w_w, 2)
    #    vertail_lines = self.draw_lines(values, c_w_w, part)
    #    vl = []
    #    gaps = []
    #    for i in range(len(vertail_lines)):
    #        vl.append(vertail_lines[i].length)
    #        if i >= 1:
    #            vertail_lines[i - 1].gap = vertail_lines[i].start - vertail_lines[i-1].start - vertail_lines[i-1].length
    #            gaps.append(vertail_lines[i-1].gap)
    #
    #    vl = concentrated(vl, 1)
    #
    #   
    #    print('gaps =', gaps)

        

    # 将有意义的黑色像素，画出来，判断边界.
    def draw_lines(self, values, projection, part):
        withe, ws, black, bs = values
        withe_min = max(0, withe - ws)
        withe_max = withe + ws
        lines = []
        start = -1
        h = 0

        for i in range(len(projection)):
            value =  projection[i]
            if value >= withe_min and value <= withe_max :
                if start == -1:
                    continue
                else: 
                    # 结束，
                    line = Line(start, h)
                    lines.append(line)
                    start = -1
            else:
                if start == -1:
                    start = i
                    h = 1
                else:
                    h = h + 1
        
        return lines



        
 
if __name__=='__main__':
    img = cv2.imread("./imgs/1.png", 0)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    choiceClassifier = ChoiceClassifier(img, (242, 709, 1057, 188), [1])
    choiceClassifier.classifier()