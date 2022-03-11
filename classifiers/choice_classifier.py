

from classifier import Classifier
import cv2
from rect import get_gaps
from util.projection import Y_Project, X_Project
from util.data import get_lines, get_max_value, filter_zero, get_site_value, split_list_to_group_idx, is_exist_min_value, is_width_rate_of_change
import numpy as np

class ChoiceClassifier(Classifier):
    pass    

    # 先按选项是水平分布的，按层来划分.
    def classifier(self):
        self.convergency_rect()
        self.do_horization()

    # 收敛
    def convergency_rect(self):
        x, y, width, height = self.rect
        part = self.mat[y:y + height, x: x + width]
        ret,part = cv2.threshold(part, 120, 255, cv2.THRESH_BINARY)
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        h_h, h_projection = Y_Project(part)
        c_w_w = filter_zero(h_h)
        max_value = get_max_value(c_w_w)
        lines = get_lines(h_h, 1, max_value, width, False)
        y_start = lines[0].start
        y_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h

        w_w, v_projection = X_Project(part)
        c_w_w = filter_zero(w_w)
        max_value = get_max_value(c_w_w)
        lines = get_lines(w_w, 1, max_value, height, False)
        x_start = lines[0].start
        x_end = lines[len(lines) - 1].start + lines[len(lines) - 1].h
        
        part = part[y_start:y_end, x_start: x_end]
        self.mat = part
        # cv2.imwrite("./imgs/final_part.png", part)


    def do_horization(self):
        part = self.mat
        height, width = part.shape
        kernel = np.zeros((2, 2), np.uint8)
        cv2.morphologyEx(part, cv2.MORPH_OPEN, kernel)
        h_h, h_projection = Y_Project(part)
        
        #cv2.imwrite('./imgs/yy_.png', h_projection) 
       
        c_h_h = filter_zero(h_h)
        max_value = get_max_value(c_h_h)
        lines = get_lines(h_h, 1 , max_value, width, False)
        idx = 0
        for line in lines:
            print(line.start, line.h, h_h[line.start], h_h[line.start + line.h - 1])
            layer_mat = part[line.start:line.start + line.h, 0:width]
            groups, lines = self.get_layer_desc(layer_mat, idx)
            idx += 1
            direction = ""
            count = 0
            
            if len(groups):
                choice_block_idx = 0
                for g_idx  in range(len(groups)):
                    group = groups[g_idx]
                    l = len(group)
                    group_lines = lines[count: count + l]

                    if count == 0:
                        values = [group_line.h for group_line in group_lines]
                        if is_width_rate_of_change(values):
                            direction = "horizational"
                        else:
                            direction = "vertical"
                    
                    if direction == "horizational":
                        h_start = group_lines[0].start
                        h_end = group_lines[len(group_lines) - 1].start + group_lines[len(group_lines) - 1].h
                        if g_idx == len(groups) - 1:
                            layer_h, layer_w = layer_mat.shape
                            h_end = width
                        choiceMat = layer_mat[0: line.h, h_start: h_end]
                        cv2.imwrite("./imgs/choice_" + str(idx) + "_" + str(choice_block_idx) + ".png", choiceMat)

                    choice_block_idx += 1
                    count += l

    # 获取每一层的信息. 数字和选项的分类判断.
    def get_layer_desc(self, mat, index):
        # cv2.imwrite("./imgs/layer_" + str(index + 1) + ".png", mat)

        count = 0
        while True:
            # 防止死循环
            if count >= 20:
                break
            w_w, vprojection = X_Project(mat)
            cv2.imwrite("./imgs/y_projection.png", vprojection)
            c_w_w = filter_zero(w_w)
            max_value = get_max_value(c_w_w)
            height, width = mat.shape
            lines = get_lines(w_w, 1 , max_value, height, False)
            gaps = get_gaps(lines)
            # 找到合适的间隙，进行膨胀.
            gap = 2
            # print(gaps, gap, 1)
            kernel = np.ones((gap,gap),np.uint8)
            mat = cv2.erode(mat,kernel)
            w_w, vprojection = X_Project(mat)
            cv2.imwrite('./imgs/erode_' + str(count) + ".png" , vprojection)
            c_w_w = filter_zero(w_w)
            count += 1
            max_value = get_max_value(c_w_w)
            lines = get_lines(w_w, 1 , max_value, height, False)
            gaps = get_gaps(lines)
            
            if is_exist_min_value(gaps, 2) == False:
                break
        
        print(gaps, 'gaps')
        split_list = split_list_to_group_idx(gaps)
        print(split_list)
        return split_list, lines


if __name__=='__main__':
    img = cv2.imread("./imgs/1.png", 0)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    choiceClassifier = ChoiceClassifier(img, (242, 709, 1057, 188))
    choiceClassifier.classifier()
