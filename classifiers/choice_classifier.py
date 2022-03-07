from re import S
from tracemalloc import start
import cv2
from classifier import Classifier
from project import hProject, vProject, concentrated

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
        
        self.convengence(part)
        
    # 缩减范围，收敛处理
    def convengence(self,part):
        h_h = hProject(part)
        c_h_h = [i for i in h_h]
        h_h.sort()
        # 取集中分布
        #for i in range(h_h):
        values = concentrated(h_h, 2)
        horizal_lines = self.draw_lines(values, c_h_h, part)
        hl = []
        for i in range(len(horizal_lines)):
            hl.append(horizal_lines[i].length)
            if i >= 1:
                horizal_lines[i - 1].gap = horizal_lines[i].start - horizal_lines[i-1].start - horizal_lines[i-1].length

        hl = concentrated(hl, 1)

        w_w = vProject(part)
        c_w_w = [i for i in w_w]
        w_w.sort()
        values = concentrated(w_w, 2)
        vertail_lines = self.draw_lines(values, c_w_w, part)
        vl = []
        gaps = []
        for i in range(len(vertail_lines)):
            vl.append(vertail_lines[i].length)
            if i >= 1:
                vertail_lines[i - 1].gap = vertail_lines[i].start - vertail_lines[i-1].start - vertail_lines[i-1].length
                gaps.append(vertail_lines[i-1].gap)

        vl = concentrated(vl, 1)

       
        print('gaps =', gaps)
        


        # 判断选择题方向. 
        direction = "horization"
        if hl[1] > vl[1]: # 垂直方向宽度变化多，那么先这么判断
            direction = "vertical"
        
        




        





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