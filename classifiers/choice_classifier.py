

from classifier import Classifier
import cv2
from rect import get_gaps, remove_too_large_gap_line
from util.projection import Y_Project, X_Project
from util.data import get_lines, get_middle_value, get_max_value, filter_zero, get_site_value, split_list_to_group_idx
import numpy as np

class ChoiceClassifier(Classifier):
    pass    

    # 先按选项是水平分布的，按层来划分.
    def classifier(self):
        self.convergency_rect()
       #self.do_horization()

    # 收敛
    def convergency_rect(self):
        x, y, width, height = self.rect
        part = self.mat[y:y + height, x: x + width]
        h_h, h_projection = Y_Project(part)
        c_w_w = filter_zero(h_h)
        max_value = get_max_value(c_w_w)
        lines = get_lines(h_h, 1, max_value, width)
        y_start = lines[0].start
        y_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h

        w_w, v_projection = X_Project(part)
        c_w_w = filter_zero(w_w)
        max_value = get_max_value(c_w_w)
        lines = get_lines(w_w, 1, max_value, height)
        x_start = lines[0].start
        x_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h
        part = part[y_start:y_end, x_start: x_end]
        self.mat = part
        self.do_horization()


    def do_horization(self):
        part = self.mat
        height, width = part.shape
        h_h, h_projection = Y_Project(part)
        c_h_h = filter_zero(h_h)
        middle_value = get_middle_value(c_h_h)
        max_value = get_max_value(c_h_h)
        lines = get_lines(h_h, middle_value / 3 , max_value, 1000)
        for i in range(len(lines)):
            if i == 0:
                i = 1
                line = lines[i]
                start = line.start
                h = line.h
                self.get_layer_desc(part[start:start + h, 0:width], True)

    # 获取每一层的信息. 数字和选项的分类判断.
    def get_layer_desc(self, mat, is_attempt_layer_desc):
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(mat, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite("./imgs/layer.png", mat)
        w_w, vprojection = X_Project(mat)
        cv2.imwrite("./imgs/y_projection.png", vprojection)
        c_w_w = filter_zero(w_w)
        middle_value = get_middle_value(c_w_w)
        max_value = get_max_value(c_w_w)
        height, width = mat.shape
        lines = get_lines(w_w, 1 , max_value, height)
        gaps = get_gaps(lines)
        # 找到合适的间隙，进行膨胀.
        gap = get_site_value(gaps, 8)
        print('gap value', gap)
        kernel = np.ones((gap,gap),np.uint8)
        mat = cv2.erode(mat,kernel)
        cv2.imwrite("./imgs/pp.png", mat)
        w_w, vprojection = X_Project(mat)
        cv2.imwrite('./imgs/erode.png', vprojection)
        c_w_w = filter_zero(w_w)
        middle_value = get_middle_value(c_w_w)
        max_value = get_max_value(c_w_w)
        lines = get_lines(w_w, 1 , max_value, width)
        gaps = get_gaps(lines)
        ws = []
        for i in range(len(lines)):
            ws.append(lines[i].h)
        print(ws, 'ws')
        #idx = split_list_to_group_idx(ws)
        #size = idx + 1




if __name__=='__main__':
    img = cv2.imread("./imgs/1.png", 0)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    choiceClassifier = ChoiceClassifier(img, (242, 709, 1057, 188))
    choiceClassifier.classifier()
