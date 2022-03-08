
from project import vProject
import cv2
from rect import Rect, sort_y, sort_x
class OptionClassifier():
    def set_direction(self, direction):
        self.direction = direction

    def classifier(self, mat):
        if self.direction == "horition":
            print('horition')
        else: 
            print('vertica')

        # 对v_project进行逻辑处理.
        w_w, v_project = vProject(mat)
        contours, hierarchy = cv2.findContours(v_project,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        x_rects = []
        
        print(len(contours))
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

        print(gaps, 'gaps', ws)


    # 得到最小的矩形框
    def get_min_rect(self, mat, rect):
        print('get_min_rect')
